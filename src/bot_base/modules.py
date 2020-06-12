import importlib
import os
import sys

import toml
from packaging.specifiers import SpecifierSet
import errors
from config import config_types
from config.base import BaseType
from config.config_types import factory
import typing

MINIMAL_INFOS = ["version", "bot_version"]

__version__ = "0.2.0"

class Dependency:
    def __init__(self, name, version):
        self.name = name
        self.version = version


class Module:
    def __init__(self, module_manager, name):
        self.name = name
        self.module_manager = module_manager
        self.__infos = None
        self.__path = os.path.join(self.module_manager.config["modules_folder"], name)

        self.__module = None
        self.__class = None
        self.__dispatch = lambda *x, **y: None

    def dispatch(self, *args, **kwargs):
        return self.__dispatch(*args, **kwargs)

    @property
    def version(self):
        """Get version of module"""
        return self.infos.get("version")

    @property
    def exists(self):
        """Check if module exists"""
        return os.path.isdir(self.__path)

    @property
    def has_infos(self):
        """Check if module contains all necessary files"""
        if not self.exists:
            raise errors.ModuleNotFoundError(f"Module {self.name} not found here: {self.__path}.")
        return os.path.isfile(os.path.join(self.__path, "infos.toml"))

    @property
    def infos(self):
        if not self.has_infos:
            raise errors.IncompatibleModuleError(f"Module {self.name} doesn't have infos.toml.")
        if not self.__infos:
            with open(os.path.join(self.__path, "infos.toml")) as f:
                self.__infos = toml.load(f)
        return self.__infos

    @property
    def has_all_infos(self):
        """Check if all required infos are in infos.toml"""
        for key in MINIMAL_INFOS:
            if key not in self.infos.keys():
                return False
        return True

    @property
    def is_compatible_with_client(self):
        """Check if module is compatible with bot version"""
        bot_version_specifier = SpecifierSet(self.infos["bot_version"])
        return __version__ in bot_version_specifier

    @property
    def is_metamodule(self):
        """Check if module is metamodule"""
        return self.infos.get("metamodule", False)

    @property
    def deps(self):
        deps = []
        for dep, version in self.infos.get("dependencies", dict()).items():
            deps.append(Dependency(dep, SpecifierSet(version)))
        return deps

    def load(self):
        self.__module = importlib.import_module(self.name)
        if not self.is_metamodule:
            try:
                # Try creating instance with client
                self.__class = self.__module.__main_class__(self.module_manager.client)
            except TypeError:
                self.__class = self.__module.__main_class__()
            self.__dispatch = self.__class.__dispatch__


class ModuleManager:
    def __init__(self, client):
        self.client = client
        self.modules = dict()
        self.dispatch_modules = dict()

        self.config = self.client.get_config("modules.toml")
        self.config.register("modules_folder", factory(config_types.Str))
        self.config.register("enabled_modules", factory(config_types.List, factory(config_types.Str)))

        self.config.set({
            "modules_folder": os.environ.get("LOCAL_MODULES", "modules"),
            "enabled_modules": []
        }, no_save=True)
        self.config.load()
        sys.path.insert(0, self.config["modules_folder"])

    def load_module(self, name, version=None):
        if name in self.modules.keys():
            return
        new_module = Module(self, name)
        if version is not None and new_module.version not in version:
            raise errors.MissingDependency(f"Incompatible version for dependency {name}: {new_module.version}, require {version}.")
        for dep in new_module.deps:
            self.load_module(dep.name, version=dep.version)
        new_module.load()
        self.modules.update({name: new_module})
        if not new_module.is_metamodule:
            self.dispatch_modules.update({name: new_module})
            return
        if version is None and name not in self.modules["enabled_modules"]:
            self.config.set({"enabled_modules": self.config["enabled_modules"] + [name]})
            self.config.save()

    def load_modules(self):
        for module in self.config["enabled_modules"]:
            self.load_module(module)

    def __iter__(self):
        return self.dispatch_modules.values().__iter__()
