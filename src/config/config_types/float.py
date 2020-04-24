import typing

from .base_type import BaseType


class Float(BaseType):
    #: Max value for parameter
    max: typing.Optional[float]
    #: Min value for parameter
    min: typing.Optional[float]
    #: Current value of parameter
    value: typing.Optional[float]

    def __init__(self, min: typing.Optional[float] = None, max: typing.Optional[float] = None) -> None:
        """
        Base Float type for config

        :Basic usage:

        >>> Float()
        <config_types.Float object with value None>
        >>> Float(min=0)
        <config_types.Float object with value None, min=0 max=None>
        >>> Float(max=0)
        <config_types.Float object with value None, min=None max=0>
        >>> Float(min=10, max=20)
        <config_types.Float object with value None, min=10 max=20>

        :param float min: Minimal value for parameter
        :param float max: Maximal value for parameter
        """
        self.value = None
        self.min = min
        self.max = max

    def check_value(self, value: float) -> bool:
        """
        Check if value is a correct int

        Check if value is int, and if applicable, between ``min`` and ``max`` or in ``values``

        :Basic usage:

        >>> positive = Float(min=0)
        >>> negative = Float(max=0)
        >>> ten_to_twenty = Float(min=10, max=20)
        >>> positive.check_value(0)
        True
        >>> positive.check_value(-2.143)
        False
        >>> positive.check_value(345.124)
        True
        >>> negative.check_value(0)
        True
        >>> negative.check_value(-2.1324)
        True
        >>> negative.check_value(345.124)
        False
        >>> ten_to_twenty.check_value(10)
        True
        >>> ten_to_twenty.check_value(-2.1234)
        False
        >>> ten_to_twenty.check_value(13.34)
        True
        >>> ten_to_twenty.check_value(20)
        True
        >>> ten_to_twenty.check_value(23.34)
        False

        :param float value: value to check
        :return: True if value is correct
        :rtype: bool
        """
        try:
            float(value)
        except ValueError:
            return False
        # Check min/max
        if self.min is not None and float(value) < self.min:
            return False
        if self.max is not None and float(value) > self.max:
            return False
        return True

    def set(self, value: float) -> None:
        """
        Set value of parameter

        :Basic usage:

        >>> my_float = Float(min=0)
        >>> my_float.set(34.324)
        >>> my_float.set(-34.32412) # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ValueError: ...

        :raise ValueError: if attempt to set invalid value
        :param float value: Value to set
        """
        if not self.check_value(value):
            raise ValueError("Attempt to set incompatible value.")
        self.value = float(value)

    def get(self) -> float:
        """
        Get value of parameter

        :Basic usage:

        >>> my_float = Float()
        >>> my_float.set(-3/4)
        >>> my_float.get()
        -0.75

        :return: Value of parameter
        :rtype: float
        """
        return self.value

    def to_save(self) -> float:
        """
        Build a serializable object

        :Basic usage:

        >>> my_float = Float()
        >>> my_float.to_save()
        >>> my_float.set(3/4)
        >>> my_float.to_save()
        0.75

        :return: Current value
        :rtype: float
        """
        return self.value

    def load(self, value: float):
        """
        Load serialized value

        >>> my_float = Float()
        >>> my_float.load(3/4)
        >>> my_float.get()
        0.75

        :param float value: Value to load
        """
        if not self.check_value(value):
            raise ValueError("Attempt to load incompatible value.")
        self.value = value

    def __repr__(self):
        if self.min is not None or self.max is not None:
            return f'<config_types.Float object with value {self.value}, min={self.min} max={self.max}>'
        return f'<config_types.Float object with value {self.value}>'
