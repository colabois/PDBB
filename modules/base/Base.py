"""Base class for module, never use directly !!!"""
import asyncio
import os
from typing import List, Union, Optional

import discord

from config import Config, config_types
from config.config_types import factory
from storage import Objects
from utils import emojis


class BaseClass:
    """Base class for all modules, Override it to make submodules"""
    name = ""
    help = {
        "description": "",
        "commands": {

        }
    }

    def __init__(self, client):
        """Initialize module class

        Initialize module class, always call it to set self.client when you override it.

        :param client: client instance
        :type client: LBI"""
        self.client = client
        self.objects = Objects(path=os.path.join("data", self.name.lower()))
        self.config = Config(path=os.path.join("data", self.name.lower(), "config.toml"))
        self.config.register("help_active", factory(config_types.Bool))
        self.config.register("color", factory(config_types.Color))
        self.config.register("auth_everyone", factory(config_types.Bool))
        self.config.register("authorized_roles",
                             factory(config_types.List, factory(config_types.discord_types.Role, client)))
        self.config.register("authorized_users",
                             factory(config_types.List, factory(config_types.discord_types.User, client)))
        self.config.register("command_text", factory(config_types.Str))
        self.config.register("configured", factory(config_types.Bool))
        self.config.set({"help_active": True, "color": 0x000000, "auth_everyone": False, "authorized_roles": [],
                         "authorized_users": [], "command_text": self.name.lower(), "configured": True})
        self.config.load(create=True)

    async def send_help(self, channel):
        embed = discord.Embed(
            title="[{nom}] - Aide".format(nom=self.name),
            description="*" + self.help["description"].format(prefix=self.client.config['prefix']) + "*",
            color=self.config["color"]
        )
        for command, description in self.help["commands"].items():
            embed.add_field(
                name=command.format(prefix=self.client.config['prefix'], command=self.config["command_text"]),
                value="-> " + description.format(prefix=self.client.config['prefix'],
                                                 command=self.config["command_text"]),
                inline=False)
        await channel.send(embed=embed)

    def auth(self, user: discord.User, role_list: List[int] = None, user_list: List[int] = None,
             guild: int = None):
        """
        Return True if user is an owner of the bot or in authorized_users or he have a role in authorized_roles.

        :param user: User to check
        :param user_list: List of authorized users, if not specified use self.authorized_users
        :param role_list: list of authorized roles, if not specified use self.authorized_roles
        :param guild: Specific guild to search role
        :type user_list: List[Int]
        :type role_list: List[Int]
        :type guild: Int
        :type user: discord.User
        """
        if self.config["auth_everyone"]:
            return True
        if user_list is None:
            user_list = self.config["authorized_users"] + self.client.config['admin_users']
        if user.id in user_list:
            return True
        if role_list is None:
            role_list = self.config["authorized_roles"] + self.client.config['admin_roles']
        if guild is None:
            guilds = self.client.guilds
        else:
            guilds = [guild]
        for guild in guilds:
            if guild.get_member(user.id):
                for role_id in role_list:
                    if role_id in [r.id for r in guild.get_member(user.id).roles]:
                        return True
        return False

    async def parse_command(self, message):
        """Parse a command_text from received message and execute function
        Parse message like `{prefix}{command_text} subcommand` and call class method `com_{subcommand}`.

        :param message: message to parse
        :type message: discord.Message"""
        command = self.client.config["prefix"] + (self.config["command_text"] if self.config["command_text"] else "")
        if message.content.startswith(command):
            content = message.content.split(" ", 1)[1 if " " in message.content else 0]
            sub_command, args, kwargs = self._parse_command_content(content)
            sub_command = "com_" + sub_command
            if self.auth(message.author):
                if sub_command in dir(self):
                    await self.__getattribute__(sub_command)(message, args, kwargs)
                else:
                    await self.command(message, args, kwargs)
            else:
                await self.unauthorized(message)

    @staticmethod
    def _parse_command_content(content):
        """Parse string

        Parse string like `subcommand argument "argument with spaces" -o -shortwaytopassoncharacteroption --longoption
        -o "option with argument"`. You can override this function to change parsing.

        :param content: content to parse
        :type content: str

        :return: parsed arguments: [subcommand, [arg1, arg2, ...], [(option1, arg1), (option2, arg2), ...]]
        :rtype: tuple[str, list, list]"""
        if not len(content.split()):
            return "", [], []
        # Sub_command
        sub_command = content.split()[0]
        args_ = [sub_command]
        kwargs = []
        if len(content.split()) > 1:
            # Remove subcommand
            content = content.lstrip(sub_command)
            # Take the other part of command_text
            content = content.lstrip().replace("\"", "\"\"")
            # Splitting around quotes
            quotes = [element.split("\" ") for element in content.split(" \"")]
            # Split all sub chains but raw chains and flat the resulting list
            args = [item.split() if item[0] != "\"" else [item, ] for sublist in quotes for item in sublist]
            # Second plating
            args = [item for sublist in args for item in sublist]
            # args_ are arguments, kwargs are options with arguments
            i = 0
            while i < len(args):
                if args[i].startswith("\""):
                    args_.append(args[i][1:-1])
                elif args[i].startswith("--"):
                    if i + 1 >= len(args):
                        kwargs.append((args[i].lstrip("-"), None))
                        break
                    if args[i + 1][0] != "-":
                        kwargs.append((args[i].lstrip("-"), args[i + 1].strip("\"")))
                        i += 1
                    else:
                        kwargs.append((args[i].lstrip("-"), None))
                elif args[i].startswith("-"):
                    if len(args[i]) == 2:
                        if i + 1 >= len(args):
                            break
                        if args[i + 1][0] != "-":
                            kwargs.append((args[i].lstrip("-"), args[i + 1].strip("\"")))
                            i += 1
                        else:
                            kwargs.append((args[i].lstrip("-"), None))
                    else:
                        kwargs.extend([(arg, None) for arg in args[i][1:]])
                else:
                    args_.append(args[i])
                i += 1
        return sub_command, args_, kwargs

    async def on_message(self, message: discord.Message):
        """Override this function to deactivate command_text parsing"""
        if message.author.bot:
            return
        await self.parse_command(message)

    async def command(self, message, args, kwargs):
        """Override this function to handle all messages starting with `{prefix}{command_text}`

        Function which is executed for all command_text doesn't match with a `com_{subcommand}` function"""
        await self.send_help(message.channel)

    async def com_help(self, message, args, kwargs):
        await self.send_help(message.channel)

    async def unauthorized(self, message):
        await message.channel.send("Vous n'êtes pas autorisé à effectuer cette commande")

    def dispatch(self, event, *args, **kwargs):
        # Method to call
        method = 'on_' + event
        try:
            # Try to get coro, if not exists pass without raise an error
            coro = getattr(self, method)
        except AttributeError:
            pass
        else:
            # Run event
            asyncio.ensure_future(self.client._run_event(coro, method, *args, **kwargs), loop=self.client.loop)

    async def on_error(self, event_method, *args, **kwargs):
        pass

    async def choice(self, message: discord.Message, choices: List[Union[discord.Emoji, discord.PartialEmoji, str]],
                     validation: bool = False,
                     validation_emote: Union[discord.Emoji, discord.PartialEmoji, str] = emojis.WHITE_CHECK_MARK,
                     minimal_choices: int = 1,
                     maximal_choices: Optional[int] = None,
                     timeout: Optional[float] = None,
                     user: Optional[discord.User] = None,
                     unique: bool = False):
        final_choices: List[Union[discord.Emoji, discord.PartialEmoji, str]] = []
        validation_step = False
        for emoji in choices:
            await message.add_reaction(emoji)

        def check_add(reaction, u):
            nonlocal validation_step, final_choices
            if (not user.bot) and (user is None or u.id == user.id):
                if validation_step and reaction.emoji == validation_emote:
                    return True
                if reaction in choices:
                    if not unique or reaction.emoji not in final_choices:
                        final_choices.append(reaction.emoji)
                if maximal_choices is not None and len(final_choices) > maximal_choices:
                    validation_step = False
                    asyncio.ensure_future(message.remove_reaction(validation_emote, self.client.user))
                    try:
                        asyncio.get_running_loop().run_until_complete(message.clear_reaction(validation_emote))
                    except discord.errors.Forbidden:
                        pass
                    return False
                if len(final_choices) >= minimal_choices:
                    if validation:
                        asyncio.get_running_loop().run_until_complete(message.add_reaction(validation_emote))
                        validation_step = True
                        return False
                    else:
                        return True
            return False

        def check_remove(reaction: discord.Reaction, u):
            nonlocal validation_step, final_choices
            if (not user.bot) and (user is None or u.id == user.id):
                if reaction.emoji in choices:
                    if not unique or reaction.count != 0:
                        final_choices.remove(reaction.emoji)
                    if len(final_choices) < minimal_choices:
                        if validation_step:
                            asyncio.ensure_future(message.remove_reaction(validation_emote, self.client.user))
                            try:
                                asyncio.get_running_loop().run_until_complete(message.clear_reaction(validation_emote))
                            except discord.errors.Forbidden:
                                pass
                            validation_step = False
                        return False
                    if (maximal_choices is None or len(final_choices) <= maximal_choices) and len(
                            final_choices) >= minimal_choices:
                        if validation:
                            asyncio.get_running_loop().run_until_complete(message.add_reaction(validation_emote))
                            validation_step = True
                            return False
                        else:
                            return True
            return False

        done, pending = await asyncio.wait([
            self.client.wait_for('reaction_add', timeout=timeout, check=check_add),
            self.client.wait_for('reaction_remove', timeout=timeout, check=check_remove)],
            return_when=asyncio.FIRST_COMPLETED)
        return final_choices
