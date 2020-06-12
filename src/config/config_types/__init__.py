from typing import Type

from . import discord_types
from .base_type import BaseType
from .bool import Bool
from .color import Color
from .dict import Dict
from .float import Float
from .int import Int
from .list import List
from .str import Str

__all__ = ['factory', 'Dict', 'Float', 'Int', 'List', 'Str', 'discord_types', 'Bool', 'Color']


class Meta(type):
    def __repr__(cls):
        if hasattr(cls, '__class_repr__'):
            return getattr(cls, '__class_repr__')()
        else:
            return super(Meta, cls).__repr__()


def factory(type: Type[BaseType], *args, **kwargs):
    """
    Create a new ``type`` with parameters args and kwargs

    :Basic usage:

    >>> factory(Int)
    <config_types.Int with parameters () {}>
    >>> factory(Int, min=0, max=10)
    <config_types.Int with parameters () {'min': 0, 'max': 10}>

    :param Type[BaseType] type: Type to create
    :return: New type
    """

    class Type(type, metaclass=Meta):

        def __init__(self):
            super().__init__(*args, **kwargs)

        @classmethod
        def __class_repr__(cls):
            return f"<config_types.{cls.__base__.__name__} with parameters {args} {kwargs}>"

    return Type
