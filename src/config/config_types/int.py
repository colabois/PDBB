import typing

from .base_type import BaseType


class Int(BaseType):
    #: :class:`typing.Optional` [:class:`int`]: Max value for parameter
    max: typing.Optional[int]
    #: :class:`typing.Optional` [:class:`int`]: Min value for parameter
    min: typing.Optional[int]
    #: :class:`typing.Optional` [:class:`typing.List` [:class:`int`]]: List of valid values for parameter
    values: typing.Optional[typing.List[int]]
    #: :class:`typing.Optional` [:class:`int`] Current value of parameter
    value: typing.Optional[int]

    def __init__(self, min: typing.Optional[int] = None, max: typing.Optional[int] = None,
                 values: typing.Optional[typing.List[int]] = None) -> None:
        """
        Base Int type for config

        :Basic usage:

        >>> Int()
        <config_types.Int object with value None>
        >>> Int(min=0)
        <config_types.Int object with value None, min=0 max=None>
        >>> Int(max=0)
        <config_types.Int object with value None, min=None max=0>
        >>> Int(min=10, max=20)
        <config_types.Int object with value None, min=10 max=20>
        >>> Int(values=[2, 3, 5, 7])
        <config_types.Int object with value None, values=[2, 3, 5, 7]>
        >>> Int(min=0, values=[3, 4, 5]) # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ValueError: ...

        :raise ValueError: If min and/or max are set when using values
        :param typing.Optional[int] min: Min value for this parameter
        :param typing.Optional[int] max: Max value for this parameter
        :param typing.Optional[typing.List[int]] values: This parameter can only be in one of these values (raise ValueError if min or max are set with values)
        """
        self.value = None
        if values is not None and (min is not None or max is not None):
            raise ValueError("Il n'est pas possible de définir un champ avec à "
                             "la fois un max/min et une série de valeur")
        self.values = values
        self.min = min
        self.max = max

    def check_value(self, value: int) -> bool:
        """
        Check if value is a correct int

        Check if value is int, and if applicable, between ``min`` and ``max`` or in ``values``

        :Basic usage:

        >>> positive = Int(min=0)
        >>> negative = Int(max=0)
        >>> ten_to_twenty = Int(min=10, max=20)
        >>> prime = Int(values=[2,3,5,7])
        >>> positive.check_value(0)
        True
        >>> positive.check_value(-2)
        False
        >>> positive.check_value(345)
        True
        >>> negative.check_value(0)
        True
        >>> negative.check_value(-2)
        True
        >>> negative.check_value(345)
        False
        >>> ten_to_twenty.check_value(10)
        True
        >>> ten_to_twenty.check_value(-2)
        False
        >>> ten_to_twenty.check_value(20)
        True
        >>> prime.check_value(2)
        True
        >>> prime.check_value(4)
        False
        >>> prime.check_value(5)
        True

        :param int value: value to check
        :return bool: True if value is correct
        """
        try:
            int(value)
        except ValueError:
            return False
        # Check min/max
        if self.min is not None and int(value) < self.min:
            return False
        if self.max is not None and int(value) > self.max:
            return False
        # Check validity
        if self.values is not None and value not in self.values:
            return False
        return True

    def set(self, value: int) -> None:
        """
        Set value of parameter

        :Basic usage:

        >>> my_int = Int(min=0)
        >>> my_int.set(34)
        >>> my_int.set(-34) # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ValueError: ...

        :raise ValueError: if attempt to set invalid value
        :param int value: Value to set
        """
        if not self.check_value(value):
            raise ValueError("Attempt to set incompatible value.")
        self.value = int(value)

    def get(self) -> typing.Optional[int]:
        """
        Get value of parameter

        :Basic usage:

        >>> my_int = Int()
        >>> my_int.set(34)
        >>> my_int.get()
        34

        :return: Value of parameter
        :rtype: Optional[int]
        """
        return self.value

    def to_save(self) -> int:
        """
        Build a serializable object

        :Basic usage:

        >>> my_int = Int()
        >>> my_int.to_save()
        >>> my_int.set(34)
        >>> my_int.to_save()
        34

        :return: Current value
        :rtype: int
        """
        return self.value

    def load(self, value: int) -> None:
        """
        Load serialized value

        >>> my_int = Int()
        >>> my_int.load(34)
        >>> my_int.get()
        34

        :param int value: Value to load
        """
        if not self.check_value(value):
            raise ValueError("Attempt to load incompatible value.")
        self.value = value

    def __repr__(self):
        if self.min is not None or self.max is not None:
            return f'<config_types.Int object with value {self.value}, min={self.min} max={self.max}>'
        if self.values:
            return f'<config_types.Int object with value {self.value}, values={self.values}>'
        return f'<config_types.Int object with value {self.value}>'
