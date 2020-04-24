from __future__ import annotations

import typing

import discord

from config.config_types.base_type import BaseType

if typing.TYPE_CHECKING:
    from bot_base import BotBase


class Channel(BaseType):
    client: BotBase

    def __init__(self, client):
        self.value = 0
        self.channel_instance = None
        self.client = client

    def check_value(self, value):
        id = value
        if isinstance(value, discord.Guild):
            id = value.id
        if not self.client.is_ready():
            self.client.warning(f"No check for channel {value} because client is not initialized!")
            return True
        if self.client.get_channel(id):
            return True
        return True

    def set(self, value):
        if not self.check_value(value):
            raise ValueError("Attempt to set incompatible value.")
        self.value = value
        self._update()

    def get(self):
        if self.channel_instance is None:
            self._update()
        return self.channel_instance or self.value

    def to_save(self):
        return self.value or 0

    def load(self, value):

        if self.check_value(value):
            raise ValueError("Attempt to load incompatible value.")
        self.set(value)
        self._update()

    def _update(self):
        if self.client.is_ready() and self.channel_instance is None:
            self.channel_instance = self.client.get_channel(self.value)
        else:
            self.channel_instance = None

