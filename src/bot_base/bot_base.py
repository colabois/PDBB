from __future__ import annotations

import asyncio
import logging
import os
import traceback

import discord
from aiohttp import web

from bot_base.modules import ModuleManager
from config import Config, config_types
from config.config_types import factory

__version__ = "0.2.0"


class BotBase(discord.Client):
    log = None

    def __init__(self, data_folder: str = "data", modules_folder: str = "modules", *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Create folders
        os.makedirs(modules_folder, exist_ok=True)
        os.makedirs(data_folder, exist_ok=True)
        # Add module folder to search path
        # TODO: Vérifier que ca ne casse rien
        # Setup logging
        self.log = logging.getLogger('bot_base')

        # Setup config
        self.configs = {}

        self.config = Config(path=os.path.join(data_folder, "config.toml"))
        self.config.register("data_folder", factory(config_types.Str))
        self.config.register("port", factory(config_types.Int))

        self.config.set({
            "data_folder": data_folder,
            "port": 8080,
        }, no_save=True)

        self.config.load()

        self.modules = ModuleManager(self)

        self.webserver = web.Application()
        self.loop.create_task(web._run_app(self.webserver, port=self.config["port"]), name="webserver")

    async def on_ready(self):
        self.info("Bot ready.")
        self.modules.load_modules()

    def dispatch(self, event, *args, **kwargs):
        """Dispatch event"""
        super().dispatch(event, *args, **kwargs)
        for module in self.modules:
            module.dispatch(event, *args, **kwargs)

    async def on_error(self, event_method, *args, **kwargs):
        self.error(f"Error in {event_method}: \n{traceback.format_exc()}")

    # Logging
    def info(self, info, *args, **kwargs):
        if self.log:
            self.log.info(info, *args, **kwargs)
        self.dispatch("log_info", info, *args, **kwargs)

    def error(self, e, *args, **kwargs):
        if self.log:
            self.log.error(e, *args, **kwargs)
        self.dispatch("log_error", e, *args, **kwargs)

    def warning(self, warning, *args, **kwargs):
        if self.log:
            self.log.warning(warning, *args, **kwargs)
        self.dispatch("log_warning", warning, *args, **kwargs)

    # Configuration

    def get_config(self, path):
        path = os.path.join(self.config["data_folder"], path)
        config = self.configs.get(path) or Config(path=path)
        self.configs.update({
            path: config
        })
        return config
