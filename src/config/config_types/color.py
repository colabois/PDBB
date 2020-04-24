import typing

from .base_type import BaseType


class Color(BaseType):
    #: :class:`typing.Optional` [:class:`int`]: Current value
    value: typing.Optional[int]

    def __init__(self) -> None:
        """
        Base Color type for config

        :Basic usage:

        >>> Color()
        <config_types.Color object with value None>
        """
        self.value = None

    def check_value(self, value: int) -> bool:
        """
        Check if value is a correct bool

        Check if value is int, and if applicable, between ``min`` and ``max`` or in ``values``

        :Basic usage:

        >>> my_color = Color()
        >>> my_color.check_value(0xFF00FF)
        True
        >>> my_color.check_value(-2)
        False
        >>> my_color.check_value(345)
        True
        >>> my_color.check_value(0xFFFFFF)
        True
        >>> my_color.check_value(0x000000)
        True
        >>> my_color.check_value(0x1000000)
        False

        :param int value: value to check
        :return: True if value is correct
        :rtype: bool
        """
        try:
            int(value)
        except ValueError:
            return False
        return 0xFFFFFF >= value >= 0x000000

    def set(self, value: int) -> None:
        """
        Set value of parameter

        :Basic usage:

        >>> my_color = Color()
        >>> my_color.set(34)

        :param int value: Value to set
        """
        if not self.check_value(value):
            raise ValueError("Attempt to set incompatible value.")
        self.value = int(value)

    def get(self) -> typing.Optional[int]:
        """
        Get value of parameter

        :Basic usage:

        >>> my_color = Color()
        >>> my_color.set(34)
        >>> my_color.get()
        34

        :return: Value of parameter
        :rtype: typing.Optional[int]
        """
        return self.value

    def to_save(self) -> int:
        """
        Build a serializable object

        :Basic usage:

        >>> my_color = Color()
        >>> my_color.to_save()
        >>> my_color.set(34)
        >>> my_color.to_save()
        34

        :return: Current value
        :rtype: int
        """
        return self.value

    def load(self, value: int) -> None:
        """
        Load serialized value

        >>> my_color = Color()
        >>> my_color.load(True)
        >>> my_color.get()
        True

        :param int value: Value to load
        """
        if not self.check_value(value):
            raise ValueError("Attempt to load incompatible value.")
        self.value = value

    def __repr__(self):
        return f'<config_types.Color object with value {self.value}>'
