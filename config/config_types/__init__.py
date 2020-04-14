from typing import Type

from config.config_types.base_type import BaseType
from config.config_types.dict import Dict
from config.config_types.float import Float
from config.config_types.int import Int
from config.config_types.list import List
from config.config_types.str import Str

__all__ = ['factory', "BaseType", 'Dict', 'Float', 'Int', 'List', 'Str']


def factory(type: Type[BaseType], *args, **kwargs):
    """
    Create a new test ``type`` with parameters args and kwargs

    :Basic usage:

    >>> factory(Int) # doctest: +ELLIPSIS
    <class '...'>
    >>> factory(Int, min=0, max=10) # doctest: +ELLIPSIS
    <class '...'>

    :param type: Type to create
    :return: New type
    """

    class Type(type):
        def __init__(self):
            super().__init__(*args, **kwargs)

    return Type
