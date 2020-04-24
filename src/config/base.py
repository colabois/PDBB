from __future__ import annotations

import os
import typing

import toml

BaseType = typing.TypeVar("BaseType")


class Config:
    #: :class:`str`: Path of config file
    path: str

    #: :class:`typing.Type` [:class:`BaseType`]: Current fields
    fields: typing.Dict[str, BaseType]

    def __init__(self, path: str) -> None:
        """
        Create config object

        Basic usage:

        >>> config = Config("doctest_config.toml")

        :param str path: Path of config file
        """
        self.fields = {}
        self.path = path

    def register(self, name: str, type_: typing.Type[BaseType]) -> None:
        """
        Register option

        Basic usage:

        >>> from config.config_types import factory, Int
        >>> config = Config("doctest_config.toml")
        >>> config.register("my_parameter", factory(Int))

        :param str name: Name of config parameter
        :param typing.Type[BaseType] type_: Type of config parameter
        """
        self.fields.update({
            name: type_()
        })

    def set(self, values: dict) -> None:
        """
        Set all parameters with values (and override old ones)

        Basic usage:

        >>> from config.config_types import factory, Int
        >>> config = Config("doctest_config.toml")
        >>> config.register("my_parameter", factory(Int))
        >>> config.set({"my_parameter": 3})

        :type values: dict
        :param values: dict of parameters
        """
        for k, v in values.items():
            try:
                self.fields[k].set(v)
            except KeyError:
                # TODO: trouver un moyen de warn
                pass

    def save(self) -> None:
        """
        Save config to ``self.file``

        Basic usage:

        >>> from config.config_types import factory, Int
        >>> config = Config("doctest_config.toml")
        >>> config.register("my_parameter", factory(Int))
        >>> config.set({"my_parameter": 3})
        >>> config.save() #doctest: +SKIP
        """
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, 'w') as file:
            toml.dump({k: v.to_save() for k, v in self.fields.items()}, file)

    def load(self) -> None:
        """
        Load config from ``self.file``

        Basic usage:

        >>> from config.config_types import factory, Int
        >>> config = Config("doctest_config.toml")
        >>> config.register("my_parameter", factory(Int))
        >>> config.set({"my_parameter": 3})
        >>> config.save() #doctest: +SKIP
        >>> new_config = Config("doctest_config.toml")
        >>> new_config.register("my_parameter", factory(Int))
        >>> new_config.load() #doctest: +SKIP
        >>> new_config["my_parameter"] #doctest: +SKIP
        3

        :return: None
        """
        try:
            with open(self.path, 'r') as file:
                self.set(toml.load(file))
        except FileNotFoundError:
            pass
        self.save()

    def __getitem__(self, item: str) -> typing.Any:
        """
        Get field from config

        :param str item: Config field to get

        Basic usage:

        >>> from config.config_types import factory, Int
        >>> config = Config("doctest_config.toml")
        >>> config.register("my_parameter", factory(Int))
        >>> config.set({"my_parameter": 3})
        >>> print(config["my_parameter"])
        3
        """
        return self.fields[item].get()
