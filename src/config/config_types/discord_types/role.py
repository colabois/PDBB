from __future__ import annotations
import typing

from config.config_types.base_type import BaseType
if typing.TYPE_CHECKING:
    from bot_base import BotBase


class Role(BaseType):
    client: BotBase

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
