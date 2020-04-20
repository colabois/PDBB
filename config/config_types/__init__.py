from typing import Type

import config.config_types.discord_types
from config.config_types.base_type import BaseType
from config.config_types.bool import Bool
from config.config_types.color import Color
from config.config_types.dict import Dict
from config.config_types.float import Float
from config.config_types.int import Int
from config.config_types.list import List
from config.config_types.str import Str

__all__ = ['factory', "BaseType", 'Dict', 'Float', 'Int', 'List', 'Str', 'discord_types', 'Bool', 'Color']


class Meta(type):
    def __repr__(cls):
        if hasattr(cls, '__class_repr__'):
            return getattr(cls, '__class_repr__')()
        else:
            return super(Meta, cls).__repr__()


def factory(type: Type[BaseType], *args, **kwargs):
    """
    Create a new test ``type`` with parameters args and kwargs

    :Basic usage:

    >>> factory(Int)
    <config_types.Int with parameters () {}>
    >>> factory(Int, min=0, max=10)
    <config_types.Int with parameters () {'min': 0, 'max': 10}>

    :param type: Type to create
    :return: New type
    """

    class Type(type, metaclass=Meta):

        def __init__(self):
            super().__init__(*args, **kwargs)

        @classmethod
        def __class_repr__(cls):
            return f"<config_types.{cls.__base__.__name__} with parameters {args} {kwargs}>"

    return Type
