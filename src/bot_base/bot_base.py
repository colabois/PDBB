from __future__ import annotations

import importlib
import inspect
import logging
import os
import sys

import discord
import toml
from packaging.specifiers import SpecifierSet

from config import Config, config_types
from config.config_types import factory
from errors import IncompatibleModuleError

__version__ = "0.1.0"
MINIMAL_INFOS = ["version", "bot_version"]


class BotBase(discord.Client):
    log = None

    def __init__(self, data_folder: str = "data", modules_folder: str = "modules", *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Create folders
        os.makedirs(modules_folder, exist_ok=True)
        os.makedirs(data_folder, exist_ok=True)
        # Add module folder to search path
        # TODO: Vérifier que ca ne casse rien
        sys.path.insert(0, modules_folder)
        # Setup logging
        self.log = logging.getLogger('bot_base')
        # Content: {"module_name": {"module": imported module, "class": initialized class}}
        self.modules = {}

        # Setup config
        self.config = Config(path=os.path.join(data_folder, "config.toml"))
        self.config.register("modules", factory(config_types.List, factory(config_types.Str)))
        self.config.register("prefix", factory(config_types.Str))
        self.config.register("admin_roles", factory(config_types.List, factory(config_types.discord_types.Role, self)))
        self.config.register("admin_users", factory(config_types.List, factory(config_types.discord_types.User, self)))
        self.config.register("main_guild", factory(config_types.discord_types.Guild, self))
        self.config.register("locale", factory(config_types.Str))
        self.config.register("data_folder", factory(config_types.Str))
        self.config.register("modules_folder", factory(config_types.Str))

        self.config.set({
            "modules": [],
            "prefix": "%",
            "admin_roles": [],
            "admin_users": [],
            "main_guild": None,
            "locale": "fr_FR.UTF8",
            "data_folder": data_folder,
            "modules_folder": modules_folder,
        })

        self.config.load()
        self.load_module("test_module")

    async def on_ready(self):
        self.info("Bot ready.")

    def load_module(self, module: str) -> None:
        """
        Try to load module

        :raise ModuleNotFoundError: If module is not in module folder
        :raise IncompatibleModuleError: If module is incompatible
        :param str module: module to load
        """
        # Check if module exists
        if not os.path.isdir(os.path.join(self.config["modules_folder"], module)):
            raise ModuleNotFoundError(f"Module {module} not found in modules folder ({self.config['modules_folder']}.)")
        if not os.path.isfile(os.path.join(self.config["modules_folder"], module, "infos.toml")):
            raise IncompatibleModuleError(f"Module {module} is incompatible: no infos.toml found.")
        # Check infos.toml integrity
        with open(os.path.join(self.config["modules_folder"], module, "infos.toml")) as f:
            infos = toml.load(f)
        for key in MINIMAL_INFOS:
            if key not in infos.keys():
                raise IncompatibleModuleError(f"Missing information for module {module}: missing {key}.")
        # Check bot_version
        bot_version_specifier = SpecifierSet(infos["bot_version"])
        if __version__ not in bot_version_specifier:
            raise IncompatibleModuleError(f"Module {module} is not compatible with your current bot version "
                                          f"(need {infos['bot_version']} and you have {__version__}).")
        # Check if module have __main_class__
        imported = importlib.import_module(module)
        try:
            main_class = imported.__main_class__
        except AttributeError:
            raise IncompatibleModuleError(f"Module {module} does not provide __main_class__.")
        # Check if __main_class__ is a class
        if not inspect.isclass(main_class):
            raise IncompatibleModuleError(f"Module {module} contains __main_class__ but it is not a type.")
        try:
            main_class = main_class(self)
        except TypeError:
            # Module don't need client reference
            main_class = main_class()
        # Check if __main_class__ have __dispatch__ attribute
        try:
            dispatch = main_class.__dispatch__
        except AttributeError:
            raise IncompatibleModuleError(f"Module {module} mainclass ({main_class}) does not provide __dispatch__"
                                          f" attribute)")
        # Check if __dispatch__ is function
        if not inspect.isfunction(imported.__main_class__.__dispatch__):
            raise IncompatibleModuleError(f"Module {module} mainclass ({main_class}) provides __dispatch__, but it is "
                                          f"not a function ({dispatch}).")
        # Check if __dispatch__ can have variable positional and keyword aguments (to avoid future error on each event)
        sig = inspect.signature(dispatch)
        args_present, kwargs_present = False, False
        for p in sig.parameters.values():
            if p.kind == p.VAR_POSITIONAL:
                args_present = True
            elif p.kind == p.VAR_KEYWORD:
                kwargs_present = True
        if not args_present:
            raise IncompatibleModuleError(
                f"Module {module} mainclass ({main_class}) provide __dispatch__ function, but "
                f"this function doesn't accept variable positionnal arguments.")
        if not kwargs_present:
            raise IncompatibleModuleError(
                f"Module {module} mainclass ({main_class}) provide __dispatch__ function, but "
                f"this function doesn't accept variable keywords arguments.")
        # Module is compatible!
        # Add module to loaded modules

        self.modules.update({
            module: {
                "imported": imported,
                "initialized_class": main_class,
                "dispatch": dispatch,
            }
        })

    def dispatch(self, event, *args, **kwargs):
        """Dispatch event"""
        super().dispatch(event, *args, **kwargs)
        for module in self.modules.values():
            module["dispatch"](event, *args, **kwargs)

    # Logging
    def info(self, *args, **kwargs):
        if self.log:
            self.log.info(*args, **kwargs)
        self.dispatch("on_log_info", *args, **kwargs)

    def error(self, *args, **kwargs):
        if self.log:
            self.log.error(*args, **kwargs)
        self.dispatch("on_log_error", *args, **kwargs)

    def warning(self, *args, **kwargs):
        if self.log:
            self.log.warning(*args, **kwargs)
        self.dispatch("on_log_warning", *args, **kwargs)
