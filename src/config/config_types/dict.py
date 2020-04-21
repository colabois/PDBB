import typing

from config.config_types.base_type import BaseType


class Dict(BaseType):
    #: :class:`typing.Type` [:class:`BaseType`]: Type for key
    type_key: typing.Type[BaseType]
    #: :class:`typing.Type` [:class:`BaseType`]: Type for value
    type_value: typing.Type[BaseType]

    def __init__(self, type_key: typing.Type[BaseType], type_value: typing.Type[BaseType]):
        """
        Config type for dictionnary

        :Basic usage:

        >>> from config.config_types import factory, Int, Float
        >>> Dict(factory(Int), factory(Float))
        <config_types.Dict<<config_types.Int with parameters () {}>: <config_types.Float with parameters () {}>> object with value None>

        :param typing.Type[BaseType] type_key: Type of keys
        :param typing.Type[BaseType] type_value: Type of values
        """
        self.type_key = type_key
        self.type_value = type_value
        self.values = None

    def check_value(self, value: typing.Dict[typing.Any, typing.Any]) -> bool:
        """
        Check if value is good

        :Basic usage:

        >>> from config.config_types import factory, Int, Float
        >>> my_dict = Dict(factory(Int), factory(Float))
        >>> my_dict.check_value("ere")
        False
        >>> my_dict.check_value(23)
        False
        >>> my_dict.check_value({23:0.75})
        True
        >>> my_dict.check_value({"er":0.75})
        False
        >>> my_dict.check_value({34:"er"})
        False

        :param typing.Dict[typing.Any, typing.Any] value: Value to check
        :return: True if value is correct
        :rtype: bool
        """
        o_key = self.type_key()
        o_value = self.type_value()
        if type(value) == dict:
            for k, v in value.items():
                if not (o_key.check_value(k) and o_value.check_value(v)):
                    return False
            return True
        return False

    def set(self, value: typing.Dict[typing.Any, typing.Any]) -> None:
        """
        Set value

        :Basic usage:

        >>> from config.config_types import factory, Int, Float
        >>> my_dict = Dict(factory(Int), factory(Float))
        >>> my_dict.set({34: 0.75})
        >>> my_dict.set("error") # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ValueError: ...

        :raise ValueError: if attempt to set invalid value
        :param typing.Dict[typing.Any, typing.Any] value: Value to set
        """
        new_dict = dict()
        if not self.check_value(value):
            raise ValueError("Tentative de définir une valeur incompatible")
        for k, v in value.items():
            new_key = self.type_key()
            new_key.set(k)
            new_value = self.type_value()
            new_value.set(v)
            new_dict.update({new_key: new_value})
        self.values = new_dict

    def get(self) -> typing.Dict[typing.Any, typing.Any]:
        """
        Get value

        :Basic usage:

        >>> from config.config_types import factory, Int, Float
        >>> my_dict = Dict(factory(Int), factory(Float))
        >>> my_dict.set({34: 0.75})
        >>> my_dict.get()
        {34: 0.75}

        :return: Current value
        :rtype: typing.Dict[typing.Any, typing.Any]
        """
        if self.values is not None:
            return {k.get(): v.get() for k, v in self.values.items()}
        return dict()

    def to_save(self) -> typing.List[typing.List[typing.Any]]:
        """
        Build a serializable data to save

        >>> from config.config_types import factory, Int, Float
        >>> my_dict = Dict(factory(Int), factory(Float))
        >>> my_dict.set({34: 0.75})
        >>> my_dict.to_save()
        [[34, 0.75]]

        :return: Dict as list of key, value tuples
        :rtype: typing.List[typing.List[typing.Any]]
        """
        # Construction d'une liste de liste: [[key, value], ...]
        if self.values is not None:
            return [[k.to_save(), v.to_save()] for k, v in self.values.items()]
        return list()

    def load(self, value: typing.List[typing.List[typing.Any]]) -> None:
        """
        Load value from saved data

        :Basic usage:

        >>> from config.config_types import factory, Int, Float
        >>> my_dict = Dict(factory(Int), factory(Float))
        >>> my_dict.load([[34, 0.75]])
        >>> my_dict.get()
        {34: 0.75}

        :param typing.List[typing.List[typing.Any]] value:
        """
        new_values = dict()
        for v in value:
            new_key = self.type_key()
            new_key.load(v[0])
            new_value = self.type_value()
            new_value.load(v[1])
            new_values.update({new_key: new_value})
        self.values = new_values

    def __repr__(self):
        return f'<config_types.Dict<{self.type_key}: {self.type_value}> object with value {self.values}>'
