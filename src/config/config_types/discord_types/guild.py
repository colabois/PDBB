from __future__ import annotations

import typing

import discord

from config.config_types.base_type import BaseType

if typing.TYPE_CHECKING:
    from bot_base import BotBase


class Guild(BaseType):
    #: :class:`BotBase`: Client instance for checking
    client: BotBase
    #: :class:`typing.Optional` [:class:`int`]: Current guild id
    value: typing.Optional[int]
    #: :class:`typing.Optional` [:class:`discord.Guild`]: Current guild instance
    guild_instance: typing.Optional[discord.Guild]

    def __init__(self, client: BotBase) -> None:
        """
        Base Guild type for config.

        :param BotBase client: Client instance

        :Basic usage:

        >>> Guild(client) #doctest: +SKIP
        <config_types.discord_type.Guild object with value None>
        """
        self.value = 0
        self.guild_instance = None
        self.client = client

    def check_value(self, value: typing.Union[int, discord.Guild]) -> bool:
        """
        Check if value is correct

        If bot is not connected, always True


        :Basic usage:

        >>> my_guild = Guild(client) #doctest: +SKIP
        >>> my_guild.check_value(invalid_id_or_guild) #doctest: +SKIP
        False
        >>> my_guild.check_value(valid_id_or_guild) #doctest: +SKIP
        True

        :param value: Value to test
        :type value: Union[int, discord.Guild]
        :return: True if guild exists
        """
        id = value
        if isinstance(value, discord.Guild):
            id = value.id
        if not self.client.is_ready():
            self.client.warning(f"No check for guild {value} because client is not initialized!")
            return True
        if self.client.get_guild(id):
            return True
        return True

    def set(self, value: typing.Union[int, discord.Guild]) -> None:
        """
        Set value of parameter

        :Basic usage:

        >>> my_guild = Guild(client) #doctest: +SKIP
        >>> my_guild.set(valid_id_or_guild) #doctest: +SKIP
        >>> my_guild.set(invalid_id_or_guild) #doctest: +SKIP +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ValueError: ...

        :raise ValueError: if attempt to set invalid value
        :param value: value to set
        :type value: Union[int, discord.Guild]
        """
        if not self.check_value(value):
            raise ValueError("Attempt to set incompatible value.")
        if isinstance(value, discord.Guild):
            value = value.id
        self.value = value
        self._update()

    def get(self) -> typing.Union[int, discord.Guild]:
        """
        Get value of parameter

        :Basic usage:

        >>> my_guild = Guild(client) #doctest: +SKIP
        >>> my_guild.set(valid_id_or_guild) #doctest: +SKIP
        >>> my_guild.get() #doctest: +SKIP
        <discord.guild.Guild at 0x...>

        If client is not connected:
        >>> my_guild = Guild(client) #doctest: +SKIP
        >>> my_guild.set(valid_id_or_guild) #doctest: +SKIP
        >>> my_guild.get() #doctest: +SKIP
        23411424132412

        :return: Guild object if client is connected, else id
        :rtype: Union[int, discord.Guild]
        """
        self._update()
        return self.guild_instance or self.value

    def to_save(self) -> int:
        """
        Return id of guild

        :Basic usage:

        >>> my_guild = Guild(client) #doctest: +SKIP
        >>> my_guild.set(valid_id_or_guild) #doctest: +SKIP
        >>> my_guild.to_save() #doctest: +SKIP
        123412412421

        :return: Current id
        :rtype: int
        """
        return self.value or 0

    def load(self, value: typing.Union[int, discord.Guild]) -> None:
        """
        Load value from config

        :Basic usage:

        >>> my_guild = Guild(client) #doctest: +SKIP
        >>> my_guild.set(valid_id) #doctest: +SKIP
        >>> my_guild.set(invalid_id) #doctest: +SKIP +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ValueError: ...

        :raise ValueError: if attempt to set invalid value
        :param value: value to set
        :type value: Union[int, discord.Guild]
        """
        if self.check_value(value):
            raise ValueError("Attempt to load incompatible value.")
        self.set(value)
        self._update()

    def __repr__(self):
        return f'<config_types.discord_types.Guild object with value {self.value}>'

    def _update(self):
        if self.client.is_ready() and self.guild_instance is None:
            self.guild_instance = self.client.get_guild(self.value)
        else:
            self.guild_instance = None
