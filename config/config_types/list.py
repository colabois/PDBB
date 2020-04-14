from typing import Type

from config.config_types.base_type import BaseType


class List(BaseType):
    type_: Type[BaseType]

    def __init__(self, type_, max_len=None):
        self.type_ = type_
        self.max_len = max_len
        self.values = None

    def check_value(self, value):
        new_object = self.type_()
        return new_object.check_value(value)

    def set(self, value):
        """Check and set value"""
        new_liste = []
        for v in value:
            new_element = self.type_()
            new_element.set(v)
            new_liste.append(new_element)
        self.values = new_liste

    def get(self):
        """Get value"""
        if self.values is None:
            raise ValueError("Config non initialisée")
        return [v.get() for v in self.values]

    def to_save(self):
        """Build a serializable data to save"""
        return [v.to_save() for v in self.values]

    def load(self, value):
        """Fill with value"""
        for v in value:
            new_object = self.type_()
            new_object.load(v)
            self.values.append(new_object)
