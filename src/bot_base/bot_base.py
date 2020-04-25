from __future__ import annotations

import importlib
import inspect
import logging
import os
import sys
import traceback

import discord
import toml
from packaging.specifiers import SpecifierSet

from config import Config, config_types
from config.config_types import factory
import errors

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
        self.config.register("data_folder", factory(config_types.Str))
        self.config.register("modules_folder", factory(config_types.Str))

        self.config.set({
            "modules": [],
            "data_folder": data_folder,
            "modules_folder": modules_folder,
        })

        self.config.load()

    async def on_ready(self):
        self.info("Bot ready.")
        try:
            self.load_modules()
        except errors.ModuleException as e:
            self.loop.stop()
            raise e

    def load_modules(self):
        self.info("Load modules...")
        for module in self.config["modules"]:
            if module not in self.modules.keys():
                self.load_module(module)
        self.info("Modules loaded.")

    def load_module(self, module: str) -> None:
        """
        Try to load module

        :raise ModuleNotFoundError: If module is not in module folder
        :raise IncompatibleModuleError: If module is incompatible
        :param str module: module to load
        """
        self.info(f"Attempt to load module {module}...")
        # Check if module exists
        if not os.path.isdir(os.path.join(self.config["modules_folder"], module)):
            self.warning(f"Attempt to load unknown module {module}.")
            raise errors.ModuleNotFoundError(
                f"Module {module} not found in modules folder ({self.config['modules_folder']}.)")
        if not os.path.isfile(os.path.join(self.config["modules_folder"], module, "infos.toml")):
            self.warning(f"Attempt to load incompatible module {module}: no infos.toml found")
            raise errors.IncompatibleModuleError(f"Module {module} is incompatible: no infos.toml found.")
        # Check infos.toml integrity
        with open(os.path.join(self.config["modules_folder"], module, "infos.toml")) as f:
            infos = toml.load(f)
        for key in MINIMAL_INFOS:
            if key not in infos.keys():
                self.warning(f"Attempt to load incompatible module {module}: missing information {key}")
                raise errors.IncompatibleModuleError(f"Missing information for module {module}: missing {key}.")
            # Check bot_version
        bot_version_specifier = SpecifierSet(infos["bot_version"])
        if __version__ not in bot_version_specifier:
            self.warning(f"Attempt to load incompatible module {module}: need bot version {infos['bot_version']} "
                         f"and you have {__version__}")
            raise errors.IncompatibleModuleError(f"Module {module} is not compatible with your current bot version "
                                                 f"(need {infos['bot_version']} and you have {__version__}).")
        # Check dependencies
        if infos.get("dependencies"):
            for dep, version in infos["dependencies"].items():
                if not dep in self.modules.keys():
                    self.load_module(dep)
                dep_version_specifier = SpecifierSet(version)
                if self.modules[dep]["infos"]["version"] not in dep_version_specifier:
                    self.warning(f"Attempt to load incompatible module {module}: (require {dep} ({version}) "
                                 f"and you have {dep} ({self.modules[dep]['infos']['version']})")
                    raise errors.IncompatibleModuleError(f"Module {module} is not compatible with your current install "
                                                         f"(require {dep} ({version}) and you have {dep} "
                                                         f"({self.modules[dep]['infos']['version']})")

        # Check if module is meta
        if infos.get("metamodule", False) == False:
            # Check if module have __main_class__
            try:
                imported = importlib.import_module(module)
            except Exception as e:
                self.warning(f"Attempt to load incompatible module {module}: failed import")
                raise e
            try:
                main_class = imported.__main_class__
            except AttributeError:
                self.warning(f"Attempt to load incompatible module {module}: no __main_class__ found")
                raise errors.IncompatibleModuleError(f"Module {module} does not provide __main_class__.")
            # Check if __main_class__ is a class
            if not inspect.isclass(main_class):
                self.warning(f"Attempt to load incompatible module {module}: __main_class__ is not a type")
                raise errors.IncompatibleModuleError(f"Module {module} contains __main_class__ but it is not a type.")
            try:
                main_class = main_class(self)
            except TypeError:
                # Module don't need client reference
                main_class = main_class()
            # Check if __main_class__ have __dispatch__ attribute
            try:
                dispatch = main_class.__dispatch__
            except AttributeError:
                self.warning(f"Attempt to load incompatible module {module}: __dispatch_ not found")
                raise errors.IncompatibleModuleError(
                    f"Module {module} mainclass ({main_class}) does not provide __dispatch__"
                    f" attribute)")
            # Check if __dispatch__ is function
            if not inspect.isfunction(imported.__main_class__.__dispatch__):
                self.warning(f"Attempt to load incompatible module {module}: __dispatch__ is not a function")
                raise errors.IncompatibleModuleError(
                    f"Module {module} mainclass ({main_class}) provides __dispatch__, but it is "
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
                self.warning(f"Attempt to load incompatible module {module}: __dispatch__ doesn't accept variable "
                             f"positional arguments")
                raise errors.IncompatibleModuleError(
                    f"Module {module} mainclass ({main_class}) provide __dispatch__ function, but "
                    f"this function doesn't accept variable positional arguments.")
            if not kwargs_present:
                self.warning(f"Attempt to load incompatible module {module}: __dispatch__ doesn't accept variable "
                             f"keywords arguments.")
                raise errors.IncompatibleModuleError(
                    f"Module {module} mainclass ({main_class}) provide __dispatch__ function, but "
                    f"this function doesn't accept variable keywords arguments.")
            # Module is compatible!
            # Add module to loaded modules
            self.info(f"Add modules {module} to current modules.")
            self.modules.update({
                module: {
                    "infos": infos,
                    "imported": imported,
                    "initialized_class": main_class,
                    "dispatch": dispatch,
                }
            })
        else:  # Module is metamodule
            self.info(f"Add modules {module} to current modules")
            self.modules.update({
                module: {
                    "infos": infos,
                    "dispatch": lambda *x, **y: None
                }
            })
        if module not in self.config["modules"]:
            self.config.set({"modules": self.config["modules"] + [module]})
            self.config.save()

    def dispatch(self, event, *args, **kwargs):
        """Dispatch event"""
        super().dispatch(event, *args, **kwargs)
        for module in self.modules.values():
            module["dispatch"](event, *args, **kwargs)

    async def on_error(self, event_method, exc, *args, **kwargs):
        self.error(f"Error in {event_method}: \n{exc}")

    # Logging
    def info(self, info, *args, **kwargs):
        if self.log:
            self.log.info(info, *args, **kwargs)
        self.dispatch("log_info", info, *args, **kwargs)

    def error(self, e, *args, **kwargs):
        if self.log:
            self.log.error(e, *args, **kwargs)
        self.dispatch("log_error", e, *args, **kwargs)

    def warning(self, warning, *args, **kwargs):
        if self.log:
            self.log.warning(warning, *args, **kwargs)
        self.dispatch("log_warning", warning, *args, **kwargs)
