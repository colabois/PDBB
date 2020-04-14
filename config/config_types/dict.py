from typing import Type

from config.config_types.base_type import BaseType


class Dict(BaseType):
    type_key: Type[BaseType]
    type_value: Type[BaseType]

    def __init__(self, type_key, type_value):
        self.type_key = type_key
        self.type_value = type_value
        self.values = None

    def check_value(self, value):
        """Check if value is good"""
        o_key = self.type_key()
        o_value = self.type_value()
        if type(value) == dict:
            for k, v in value.items():
                if not (o_key.check_value(k) and o_value.check_value(v)):
                    return False
            return True
        if (type(value) == list or type(value) == tuple) and len(value) == 2:
            return o_key.check_value(value[0]) and o_value.check_value(value[1])
        return False

    def set(self, value):
        """Check and set value"""
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

    def get(self):
        """Get value"""
        if self.values is not None:
            return {k.get(): v.get() for k, v in self.values.items()}
        return dict()

    def to_save(self):
        """Build a serializable data to save"""
        # Construction d'une liste de liste: [[key, value], ...]
        if self.values is not None:
            return [[k.to_save(), v.to_save()] for k, v in self.values.items()]
        return list()

    def load(self, value):
        """Fill with value"""
        new_values = dict()
        for v in value:
            new_key = self.type_key()
            new_key.load(v[0])
            new_value = self.type_value()
            new_value.load(v[1])
            new_values.update({new_key: new_value})
        self.values = new_values
