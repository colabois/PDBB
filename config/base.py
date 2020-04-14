from __future__ import annotations

from typing import Dict, Type, Any, TYPE_CHECKING

import toml

if TYPE_CHECKING:
    from config.config_types.base_type import BaseType


class Config:
    #: Path of config file
    path: str
    #: Current fields
    fields: Dict[str, BaseType]

    def __init__(self, path: str) -> None:
        """
        Create config object

        Basic usage:

        >>> config = Config("doctest_config.toml")

        :param path: Path of config file
        :type path: str
        :rtype: None
        :rtype: None
        """
        self.fields = {}
        self.path = path

    def register(self, name: str, type_: Type[BaseType]) -> None:
        """
        Register option

        Basic usage:

        >>> from config.config_types import factory, Int
        >>> config = Config("doctest_config.toml")
        >>> config.register("my_parameter", factory(Int))

        :param name: Name of config parameter
        :param type_: Type of config parameter
        :type name: str
        :type type_: Type[BaseType]
        :return: None
        :rtype: None
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
        :return: None
        :rtype: None
        """
        for k, v in values.items():
            self.fields[k].set(v)

    def save(self) -> None:
        """
        Save config to ``self.file``

        Basic usage:

        >>> from config.config_types import factory, Int
        >>> config = Config("doctest_config.toml")
        >>> config.register("my_parameter", factory(Int))
        >>> config.set({"my_parameter": 3})
        >>> config.save()

        :return: None
        """
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
        >>> config.save()
        >>> new_config = Config("doctest_config.toml")
        >>> new_config.register("my_parameter", factory(Int))
        >>> new_config.load()
        >>> new_config["my_parameter"]
        3


        :return: None
        """
        with open(self.path, 'r') as file:
            self.set(toml.load(file))

    def __getitem__(self, item: str) -> Any:
        """
        Save config to ``self.file``

        Basic usage:

        >>> from config.config_types import factory, Int
        >>> config = Config("doctest_config.toml")
        >>> config.register("my_parameter", factory(Int))
        >>> config.set({"my_parameter": 3})
        >>> print(config["my_parameter"])
        3

        :return: None
        """
        return self.fields[item].get()
