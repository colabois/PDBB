from __future__ import annotations
import typing

import discord

from config.config_types.base_type import BaseType
if typing.TYPE_CHECKING:
    from bot_base import BotBase


class User(BaseType):
    #: :class:`BotBase`: Client instance for checking
    client: BotBase
    #: :class:`typing.Optional` [:class:`int`]: Current user id
    value: int
    #: :class:`typing.Optional` [:class:`discord.User`]: Current user instance
    user_instance: typing.Optional[discord.User]

    def __init__(self, client: BotBase) -> None:
        """
        Base User type for config.

        :param BotBase client: Client instance

        :Basic usage:

        >>> User(client) #doctest: +SKIP
        <config_types.discord_type.User object with value None>
        """
        self.value = 0
        self.user_instance = None
        self.client = client

    def check_value(self, value: typing.Union[int, discord.User]) -> bool:
        """
        Check if value is correct

        If bot is not connected, always True

        :Basic usage:

        >>> my_user = User(client) #doctest: +SKIP
        >>> my_user.check_value(invalid_id_or_user) #doctest: +SKIP
        False
        >>> my_user.check_value(valid_id_or_user) #doctest: +SKIP
        True

        :param value: Value to test
        :type value: Union[int, discord.User]
        :return: True if user exists
        """
        id = value
        if isinstance(value, discord.User):
            id = value.id
        if not self.client.is_ready():
            self.client.warning(f"No check for user {value} because client is not initialized!")
            return True
        if self.client.get_user(id):
            return True
        return True

    def set(self, value: typing.Union[int, discord.User]) -> None:
        """
        Set value of parameter

        :Basic usage:

        >>> my_user = User(client) #doctest: +SKIP
        >>> my_user.set(valid_id_or_user) #doctest: +SKIP
        >>> my_user.set(invalid_id_or_user) #doctest: +SKIP +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ValueError: ...

        :raise ValueError: if attempt to set invalid value
        :param value: value to set
        :type value: Union[int, discord.User]
        """
        if not self.check_value(value):
            raise ValueError("Attempt to set incompatible value.")
        if isinstance(value, discord.User):
            value = value.id
        self.value = value
        self._update()

    def get(self) -> typing.Union[int, discord.User]:
        """
        Get value of parameter

        :Basic usage:

        >>> my_user = User(client) #doctest: +SKIP
        >>> my_user.set(valid_id_or_user) #doctest: +SKIP
        >>> my_user.get() #doctest: +SKIP
        <discord.user.User at 0x...>

        If client is not connected:
        >>> my_user = User(client) #doctest: +SKIP
        >>> my_user.set(valid_id_or_user) #doctest: +SKIP
        >>> my_user.get() #doctest: +SKIP
        23411424132412

        :return: User object if client is connected, else id
        :rtype: Union[int, discord.User]
        """
        if self.user_instance is None:
            self._update()
        return self.user_instance or self.value

    def to_save(self) -> int:
        """
        Return id of user

        :Basic usage:

        >>> my_user = User(client) #doctest: +SKIP
        >>> my_user.set(valid_id_or_user) #doctest: +SKIP
        >>> my_user.to_save() #doctest: +SKIP
        123412412421

        :return: Current id
        :rtype: int
        """
        return self.value or 0

    def load(self, value: typing.Union[int, discord.User]) -> None:
        """
        Load value from config

        :Basic usage:

        >>> my_user = User(client) #doctest: +SKIP
        >>> my_user.set(valid_id) #doctest: +SKIP
        >>> my_user.set(invalid_id) #doctest: +SKIP +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ValueError: ...

        :raise ValueError: if attempt to set invalid value
        :param value: value to set
        :type value: Union[int, discord.User]
        """
        if self.check_value(value):
            raise ValueError("Attempt to load incompatible value.")
        self.set(value)
        self._update()

    def _update(self):
        if self.client.is_ready() and self.user_instance is None:
            self.user_instance = self.client.get_user(self.value)
        else:
            self.user_instance = None

    def __repr__(self):
        return f'<config_types.discord_types.User object with value {self.value}>'