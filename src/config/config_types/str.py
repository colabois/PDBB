from .base_type import BaseType


class Str(BaseType):
    value: str

    def __init__(self) -> None:
        """
        Base Str type for config

        :Basic usage:

        >>> Str()
        <config_types.Str object with value "">
        """

        self.value = ""

    def check_value(self, value: str) -> bool:
        """
        Check if value is usable as str

        :Basic usage:

        >>> my_str = Str()
        >>> my_str.check_value("toto")
        True
        >>> my_str.check_value(45)
        True

        :param str value: Value to test
        :return: True if value is usable as str
        """
        try:
            str(value)
        except ValueError:
            return False
        return True

    def set(self, value: str) -> None:
        """
        Set value of parameter

        :Basic usage:

        >>> my_str = Str()
        >>> my_str.set("e")
        >>> my_str.set(34)

        :raise ValueError: if attempt to set invalid value
        :param str value: Value to set
        """
        if not self.check_value(value):
            raise ValueError("Attempt to set incompatible value.")
        self.value = str(value)

    def get(self) -> str:
        """
        Get value of parameter

        :Basic usage:

        >>> my_str = Str()
        >>> my_str.set(34)
        >>> print(my_str.get())
        34
        >>> my_str.set("Hey")
        >>> print(my_str.get())
        Hey

        :return: Value of parameter
        """
        return self.value

    def to_save(self) -> str:
        """
        Build a serializable data to save

        :Basic usage:

        >>> my_str = Str()
        >>> my_str.set(34)
        >>> my_str.to_save()
        '34'

        :todo: Vérifier que l'utf8 casse pas tout

        :return: Current string content
        :rtype: str
        """
        return self.value

    def load(self, value: str) -> None:
        """
        Load value

        :Basic usage:

        >>> my_str = Str()
        >>> my_str.load("34")
        >>> my_str.get()
        '34'
        """
        if not self.check_value(value):
            raise ValueError("Attempt to load incompatible value.")
        self.value = value

    def __repr__(self):
        return f'<config_types.Str object with value "{self.value}">'
