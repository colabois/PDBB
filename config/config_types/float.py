from config.config_types.base_type import BaseType


class Float(BaseType):
    def __init__(self, min_=None, max_=None):
        self.value = None
        self.min = min_
        self.max = max_

    def check_value(self, value):
        try:
            float(value)
        except ValueError:
            return False
        # TODO: < ou <=? > ou >=?
        # Check min/max
        if self.min is not None and float(value) < self.min:
            return False
        if self.max is not None and float(value) > self.max:
            return False
        return True

    def set(self, value):
        if self.check_value(value):
            self.value = value
            return
        raise ValueError("Tentative de définir une valeur incompatible")

    def get(self):
        return self.value

    def to_save(self):
        return self.value

    def load(self, value):
        if self.check_value(value):
            raise ValueError("Tentative de charger une donnée incompatible.")
        self.value = value
