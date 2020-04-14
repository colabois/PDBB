from typing import Optional, List

from config.config_types.base_type import BaseType


class Int(BaseType):
    #: Max value for parameter
    max: Optional[int]
    #: Min value for parameter
    min: Optional[int]
    #: List of valid values for parameter
    values: Optional[List[int]]
    #: Current value of parameter
    value: Optional[int]

    def __init__(self, min: Optional[int] = None, max: Optional[int] = None,
                 values: Optional[List[int]] = None) -> None:
        """
        Base Int type for config

        :Basic usage:

        >>> Int()
        <Int object with value None>
        >>> Int(min=0)
        <Int object with value None, min=0 max=None>
        >>> Int(max=0)
        <Int object with value None, min=None max=0>
        >>> Int(min=10, max=20)
        <Int object with value None, min=10 max=20>
        >>> Int(values=[2, 3, 5, 7])
        <Int object with value None, values=[2, 3, 5, 7]>
        >>> Int(min=0, values=[3, 4, 5]) # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ValueError: ...

        :raise ValueError: If min and/or max are set when using values
        :param min: Min value for this parameter
        :param max: Max value for this parameter
        :param values: This parameter can only be in one of these values (raise ValueError if min or max are set with values)
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

        :param value: value to check
        :return: True if value is correct
        """
        try:
            int(value)
        except ValueError:
            return False
        # TODO: < ou <=? > ou >=?
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
        :param value: Value to set
        :return: None
        """
        if not self.check_value(value):
            raise ValueError("Tentative de définir une valeur incompatible")
        self.value = value

    def get(self) -> Optional[int]:
        """
        Get value of parameter

        :Basic usage:

        >>> my_int = Int()
        >>> my_int.set(34)
        >>> my_int.get()
        34

        :return: Value of parameter
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
        """
        return self.value

    def load(self, value: int) -> None:
        """
        Load serialized value

        >>> my_int = Int()
        >>> my_int.load(34)
        >>> my_int.get()
        34

        :param value: Value to load
        :return: None
        """
        if not self.check_value(value):
            raise ValueError("Tentative de charger une donnée incompatible.")
        self.value = value

    def __repr__(self):
        if self.min is not None or self.max is not None:
            return f'<Int object with value {self.value}, min={self.min} max={self.max}>'
        if self.values:
            return f'<Int object with value {self.value}, values={self.values}>'
        return f'<Int object with value {self.value}>'
