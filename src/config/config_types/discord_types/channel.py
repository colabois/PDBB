from __future__ import annotations

from typing import TYPE_CHECKING

from config.config_types.base_type import BaseType

if TYPE_CHECKING:
    from main import LBI


class Channel(BaseType):
    client: LBI

    def __init__(self, client):
        self.value = None
        self.client = client

    def check_value(self, value):
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
