from config.config_types.base_type import BaseType


class Str(BaseType):
    def __init__(self):
        self.value = None

    def check_value(self, value):
        """Check if value is good"""
        try:
            str(value)
        except ValueError:
            return False
        return True

    def set(self, value):
        """Check and set value"""
        if self.check_value(value):
            self.value = value
            return
        raise ValueError("Tentative de définir une valeur incompatible")

    def get(self):
        """Get value"""
        return self.value

    def to_save(self):
        """Build a serializable data to save"""
        return self.value

    def load(self, value):
        """Fill with value"""
        if not self.check_value(value):
            raise ValueError("Tentative de charger une donnée incompatible.")
        self.value = value
