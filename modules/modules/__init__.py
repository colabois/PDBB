import os

import discord

from modules.base import BaseClass



class MainClass(BaseClass):
    name = "modules"

    command_text = "modules"
    color = 0x000000
    help = {
        "description": "Manage bot modules.",
        "commands": {
            "`{prefix}{command} list`": "List of available modules.",
            "`{prefix}{command} enable <module>`": "Enable module `<module>`.",
            "`{prefix}{command} disable <module>`": "Disable module `<module>`.",
            "`{prefix}{command} reload <module>`":"Reload module `<module>`",
            "`{prefix}{command} web_list`": "List all available modules from repository",
        }
    }

    def __init__(self, client):
        super().__init__(client)
        self.storage.mkdir("modules")

    def get_all_modules(self):
        all_items = os.listdir("modules")
        modules = []
        for item in all_items:
            if item not in ["__init__.py", "base", "__pycache__", "dummy"]:
                if os.path.isfile(os.path.join("modules", item)):
                    modules.append(item[:-3])
                else:
                    modules.append(item)
        return set(modules)

    async def com_enable(self, message, args, kwargs):
        args = args[1:]
        if len(args) == 0:
            await message.channel.send("You must specify at least one module.")
            return
        if len(args) == 1 and args[0] == "*":
            for module in self.get_all_modules():
                e = self.client.load_module(module)
                if e:
                    await message.channel.send("An error occurred during the loading of the module {module}."
                                               .format(module=module))
            await self.com_list(message, args, kwargs)
            return
        for arg in args:
            e = self.client.load_module(arg)
            if e:
                await message.channel.send("An error occurred during the loading of the module {module}."
                                           .format(module=arg))
        await self.com_list(message, args, kwargs)

    async def com_reload(self, message, args, kwargs):
        args = args[1:]
        if len(args) == 0:
            await message.channel.send("You must specify at least one module.")
            return
        if len(args) == 1 and args[0] == "*":
            for module in self.get_all_modules():
                e = self.client.unload_module(module)
                if e:
                    await message.channel.send("An error occurred during the loading of the module {module}."
                                               .format(module=module))
            await self.com_list(message, args, kwargs)
            return
        for arg in args:
            print(arg)
            e = self.client.unload_module(arg)
            if e:
                await message.channel.send("An error occurred during the loading of the module {module}."
                                           .format(module=arg))
        await self.com_list(message, [], [])

    async def com_disable(self, message, args, kwargs):
        args = args[1:]
        if len(args) == 0:
            await message.channel.send("You must specify at least one module.")
            return
        if len(args) == 1 and args[0] == "*":
            for module in self.get_all_modules():
                e = self.client.unload_module(module)
                if e:
                    await message.channel.send("An error occurred during the loading of the module {module}."
                                               .format(module=module))
            await self.com_list(message, args, kwargs)
            return
        for arg in args:
            print(arg)
            e = self.client.unload_module(arg)
            if e:
                await message.channel.send("An error occurred during the loading of the module {module}."
                                           .format(module=arg))
        await self.com_list(message, [], [])

    async def com_list(self, message, args, kwargs):
        list_files = self.get_all_modules()
        activated = set(self.client.config["modules"])
        activated_string = "\n+ " + "\n+ ".join(activated)
        deactivated_string = "- " + "\n- ".join(list_files.difference(activated))
        embed = discord.Embed(title="[Modules] - Liste des modules",
                              description="```diff\n{activated}\n{deactivated}```".format(
                                  activated=activated_string,
                                  deactivated=deactivated_string)
                              )
        await message.channel.send(embed=embed)

    async def com_web_list(self, message, args, kwargs):
        pass