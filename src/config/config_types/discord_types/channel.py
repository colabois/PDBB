from __future__ import annotations

import typing

import discord

from config.config_types.base_type import BaseType

if typing.TYPE_CHECKING:
    from bot_base import BotBase


class Channel(BaseType):
    #: :class:`BotBase`: Client instance for checking
    client: BotBase
    #: :class:`typing.Optional` [:class:`int`]: Current channel id
    value: int
    #: :class:`typing.Optional` [:class:`discord.TextChannel`]: Current channel instance
    channel_instance: typing.Optional[discord.TextChannel]

    def __init__(self, client: BotBase) -> None:
        """
        Base Channel type for config.

        :param BotBase client: Client instance

        :Basic usage:

        >>> Channel(client) #doctest: +SKIP
        <config_types.discord_type.Channel object with value None>
        """
        self.value = 0
        self.channel_instance = None
        self.client = client

    def check_value(self, value: typing.Union[int, discord.TextChannel]) -> bool:
        """
        Check if value is correct

        If bot is not connected, always True

        :Basic usage:

        >>> my_channel = Channel(client) #doctest: +SKIP
        >>> my_channel.check_value(invalid_id_or_channel) #doctest: +SKIP
        False
        >>> my_channel.check_value(valid_id_or_channel) #doctest: +SKIP
        True

        :param value: Value to test
        :type value: Union[int, discord.TextChannel]
        :return: True if channel exists
        """
        id = value
        if isinstance(value, discord.TextChannel):
            id = value.id
        if not self.client.is_ready():
            self.client.warning(f"No check for channel {value} because client is not initialized!")
            return True
        if self.client.get_channel(id):
            return True
        return True

    def set(self, value: typing.Union[int, discord.TextChannel]):
        """
        Set value of parameter

        :Basic usage:

        >>> my_channel = Channel(client) #doctest: +SKIP
        >>> my_channel.set(valid_id_or_channel) #doctest: +SKIP
        >>> my_channel.set(invalid_id_or_channel) #doctest: +SKIP +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ValueError: ...

        :raise ValueError: if attempt to set invalid value
        :param value: value to set
        :type value: Union[int, discord.TextChannel]
        """
        if not self.check_value(value):
            raise ValueError("Attempt to set incompatible value.")
        if isinstance(value, discord.TextChannel):
            value = value.id
        self.value = value
        self._update()

    def get(self) -> typing.Union[int, discord.Channel]:
        """
        Get value of parameter

        :Basic usage:

        >>> my_channel = Channel(client) #doctest: +SKIP
        >>> my_channel.set(valid_id_or_channel) #doctest: +SKIP
        >>> my_channel.get() #doctest: +SKIP
        <discord.channel.TextChannel at 0x...>

        If client is not connected:
        >>> my_channel = Channel(client) #doctest: +SKIP
        >>> my_channel.set(valid_id_or_channel) #doctest: +SKIP
        >>> my_channel.get() #doctest: +SKIP
        23411424132412

        :return: Channel object if client is connected, else id
        :rtype: Union[int, discord.Channel]
        """
        if self.channel_instance is None:
            self._update()
        return self.channel_instance or self.value

    def to_save(self) -> int:
        """
        Return id of channel

        :Basic usage:

        >>> my_channel = Channel(client) #doctest: +SKIP
        >>> my_channel.set(valid_id_or_channel) #doctest: +SKIP
        >>> my_channel.to_save() #doctest: +SKIP
        123412412421

        :return: Current id
        :rtype: int
        """
        return self.value or 0

    def load(self, value: typing.Union[int, discord.Channel]) -> None:
        """
        Load value from config

        :Basic usage:

        >>> my_channel = Channel(client) #doctest: +SKIP
        >>> my_channel.set(valid_id) #doctest: +SKIP
        >>> my_channel.set(invalid_id) #doctest: +SKIP +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ValueError: ...

        :raise ValueError: if attempt to set invalid value
        :param value: value to set
        :type value: Union[int, discord.TextChannel]
        """
        if self.check_value(value):
            raise ValueError("Attempt to load incompatible value.")
        self.set(value)
        self._update()

    def _update(self):
        if self.client.is_ready() and self.channel_instance is None:
            self.channel_instance = self.client.get_channel(self.value)
        else:
            self.channel_instance = None

    def __repr__(self):
        return f'<config_types.discord_types.Channel object with value {self.value}>'
