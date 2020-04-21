import typing

from .base_type import BaseType


class List(BaseType):
    #: :class:`typing.List` [:class:`BaseType`]: Current list of value
    values: typing.List[BaseType]
    #: :class:`typing.Type` [:class:`BaseType`]: Type of values
    type_: typing.Type[BaseType]

    def __init__(self, type_: typing.Type[BaseType]) -> None:
        """
        Base List type for config

        :Basic usage:

        >>> from config.config_types import factory, Int, Float
        >>> List(factory(Int))
        <config_types.List of <config_types.Int with parameters () {}> objects with values []>
        >>> List(factory(Float))
        <config_types.List of <config_types.Float with parameters () {}> objects with values []>

        :param typing.Type[BaseType] type_: Type of items
        """
        self.type_ = type_
        self.values = []

    def check_value(self, value: typing.List[typing.Any]) -> bool:
        """
        Check if value is correct

        :Basic usage:

        >>> from config.config_types import factory, Int
        >>> my_list = List(factory(Int))
        >>> my_list.check_value([34,])
        True
        >>> my_list.check_value(345)
        False
        >>> my_list.check_value([345, 34, 23, 45, 34, 46, 35, 2345, 'rt'])
        False

        :param typing.List[typing.Any] value: Value to check
        :return: True if value is correct
        :rtype: bool
        """
        new_object = self.type_()
        try:
            for v in value:
                if not new_object.check_value(v):
                    return False
        except TypeError:
            return False
        return True

    def set(self, value: typing.List[typing.Any]) -> None:
        """
        Set value of parameter

        :Basic usage:

        >>> from config.config_types import factory, Int
        >>> my_list = List(factory(Int))
        >>> my_list.set(34) # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ValueError: ...
        >>> my_list.set([45,])

        :param typing.List[typing.Any] value: Value to set
        """
        if not self.check_value(value):
            raise ValueError('Tentative de définir une valeur incompatible')
        new_liste = []
        for v in value:
            new_element = self.type_()
            new_element.set(v)
            new_liste.append(new_element)
        self.values = new_liste

    def get(self) -> typing.List[typing.Any]:
        """
        Get value of parameter

        :Basic usage:

        >>> from config.config_types import factory, Int
        >>> my_list = List(factory(Int))
        >>> my_list.set([34, ])
        >>> my_list.get()
        [34]

        :raise ValueError: If config is empty
        :return: Value of parameter
        :rtype: typing.List[typing.Any]
        """
        return [v.get() for v in self.values]

    def to_save(self) -> typing.List[typing.Any]:
        """
        Build a serializable object

        :Basic usage:

        >>> from config.config_types import factory, Int
        >>> my_list = List(factory(Int))
        >>> my_list.to_save()
        []
        >>> my_list.set([34, ])
        >>> my_list.to_save()
        [34]

        :return: Current value
        :rtype: typing.List[typing.Any]
        """
        return [v.to_save() for v in self.values]

    def load(self, value: typing.List[typing.Any]) -> None:
        """
        Load serialized value

        >>> from config.config_types import factory, Int
        >>> my_list = List(factory(Int))
        >>> my_list.load([34,])
        >>> my_list.get()
        [34]

        :param typing.List[typing.Any] value: Value to load
        """
        if not self.check_value(value):
            raise ValueError("Tentative de charger une donnée incompatible.")
        for v in value:
            new_object = self.type_()
            new_object.load(v)
            self.values.append(new_object)

    def __repr__(self):
        return f'<config_types.List of {self.type_} objects with values {self.values}>'
