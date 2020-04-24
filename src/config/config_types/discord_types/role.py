from __future__ import annotations
import typing

import discord

from config.config_types.base_type import BaseType
if typing.TYPE_CHECKING:
    from bot_base import BotBase


class Role(BaseType):
    #: :class:`BotBase`: Client instance for checking
    client: BotBase
    #: :class:`typing.Optional` [:class:`int`]: Current role id
    value: int
    #: :class:`typing.Optional` [:class:`discord.Role`]: Current role instance
    role_instance: typing.Optional[discord.Role]

    def __init__(self, client: BotBase) -> None:
        """
        Base Role type for config.

        :param BotBase client: Client instance

        :Basic usage:

        >>> Role(client) #doctest: +SKIP
        <config_types.discord_type.Role object with value None>
        """
        self.value = 0
        self.role_instance = None
        self.client = client

    def check_value(self, value: typing.Union[int, discord.Role]) -> bool:
        """
        Check if value is correct

        If bot is not connected, always True

        :Basic usage:

        >>> my_role = Role(client) #doctest: +SKIP
        >>> my_role.check_value(invalid_id_or_role) #doctest: +SKIP
        False
        >>> my_role.check_value(valid_id_or_role) #doctest: +SKIP
        True

        :param value: Value to test
        :type value: Union[int, discord.Role]
        :return: True if role exists
        """
        id = value
        if isinstance(value, discord.Role):
            id = value.id
        if not self.client.is_ready():
            self.client.warning(f"No check for role {value} because client is not initialized!")
            return True
        if self.client.get_role(id):
            return True
        return True

    def set(self, value: typing.Union[int, discord.Role]) -> None:
        """
        Set value of parameter

        :Basic usage:

        >>> my_role = Role(client) #doctest: +SKIP
        >>> my_role.set(valid_id_or_role) #doctest: +SKIP
        >>> my_role.set(invalid_id_or_role) #doctest: +SKIP +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ValueError: ...

        :raise ValueError: if attempt to set invalid value
        :param value: value to set
        :type value: Union[int, discord.Role]
        """
        if not self.check_value(value):
            raise ValueError("Attempt to set incompatible value.")
        if isinstance(value, discord.Role):
            value = value.id
        self.value = value
        self._update()

    def get(self) -> typing.Union[int, discord.Role]:
        """
        Get value of parameter

        :Basic usage:

        >>> my_role = Role(client) #doctest: +SKIP
        >>> my_role.set(valid_id_or_role) #doctest: +SKIP
        >>> my_role.get() #doctest: +SKIP
        <discord.role.Role at 0x...>

        If client is not connected:
        >>> my_role = Role(client) #doctest: +SKIP
        >>> my_role.set(valid_id_or_role) #doctest: +SKIP
        >>> my_role.get() #doctest: +SKIP
        23411424132412

        :return: Role object if client is connected, else id
        :rtype: Union[int, discord.Role]
        """
        if self.role_instance is None:
            self._update()
        return self.role_instance or self.value

    def to_save(self) -> int:
        """
        Return id of role

        :Basic usage:

        >>> my_role = Role(client) #doctest: +SKIP
        >>> my_role.set(valid_id_or_role) #doctest: +SKIP
        >>> my_role.to_save() #doctest: +SKIP
        123412412421

        :return: Current id
        :rtype: int
        """
        return self.value or 0

    def load(self, value: typing.Union[int, discord.Role]) -> None:
        """
        Load value from config

        :Basic usage:

        >>> my_role = Role(client) #doctest: +SKIP
        >>> my_role.set(valid_id) #doctest: +SKIP
        >>> my_role.set(invalid_id) #doctest: +SKIP +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ValueError: ...

        :raise ValueError: if attempt to set invalid value
        :param value: value to set
        :type value: Union[int, discord.Role]
        """
        if self.check_value(value):
            raise ValueError("Attempt to load incompatible value.")
        self.set(value)
        self._update()

    def _update(self):
        if self.client.is_ready() and self.role_instance is None:
            self.role_instance = self.client.get_role(self.value)
        else:
            self.role_instance = None

    def __repr__(self):
        return f'<config_types.discord_types.User object with value {self.value}>'