from typing import Optional

from config.config_types.base_type import BaseType


class Bool(BaseType):
    #: Current value of parameter
    value: Optional[bool]

    def __init__(self) -> None:
        """
        Base Bool type for config

        :Basic usage:

        >>> Bool()
        <config_types.Bool object with value None>
        """
        self.value = None

    def check_value(self, value: bool) -> bool:
        """
        Check if value is a correct bool

        Check if value is int, and if applicable, between ``min`` and ``max`` or in ``values``

        :Basic usage:

        >>> my_bool = Bool()
        >>> my_bool.check_value(0)
        True
        >>> my_bool.check_value(-2)
        True
        >>> my_bool.check_value(345)
        True
        >>> my_bool.check_value(0)
        True
        >>> my_bool.check_value(-2)
        True
        >>> my_bool.check_value(345)
        True
        >>> my_bool.check_value(10)
        True
        >>> my_bool.check_value(-2)
        True
        >>> my_bool.check_value(20)
        True
        >>> my_bool.check_value(2)
        True
        >>> my_bool.check_value(4)
        True
        >>> my_bool.check_value(5)
        True

        :param value: value to check
        :return: True if value is correct
        """
        try:
            bool(value)
        except ValueError:
            return False
        return True

    def set(self, value: bool) -> None:
        """
        Set value of parameter

        :Basic usage:

        >>> my_bool = Bool()
        >>> my_bool.set(34)

        :param value: Value to set
        :return: None
        """
        if not self.check_value(value):
            raise ValueError("Tentative de définir une valeur incompatible")
        self.value = bool(value)

    def get(self) -> Optional[int]:
        """
        Get value of parameter

        :Basic usage:

        >>> my_bool = Bool()
        >>> my_bool.set(34)
        >>> my_bool.get()
        True

        :return: Value of parameter
        """
        return self.value

    def to_save(self) -> int:
        """
        Build a serializable object

        :Basic usage:

        >>> my_bool = Bool()
        >>> my_bool.to_save()
        >>> my_bool.set(34)
        >>> my_bool.to_save()
        True

        :return: Current value
        """
        return self.value

    def load(self, value: bool) -> None:
        """
        Load serialized value

        >>> my_bool = Bool()
        >>> my_bool.load(True)
        >>> my_bool.get()
        True

        :param value: Value to load
        :return: None
        """
        if not self.check_value(value):
            raise ValueError("Tentative de charger une donnée incompatible.")
        self.value = value

    def __repr__(self):
        return f'<config_types.Bool object with value {self.value}>'
