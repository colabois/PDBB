from __future__ import annotations

import asyncio
import logging
import os
import traceback

import discord

from bot_base.modules import ModuleManager
from config import Config, config_types
from config.config_types import factory

__version__ = "0.2.0"


class BotBase():
    log = None

    def __init__(self, data_folder: str = "datas", modules_folder: str = "modules", loop = asyncio.get_event_loop()):
        # Create folders
        os.makedirs(modules_folder, exist_ok=True)
        os.makedirs(data_folder, exist_ok=True)
        self.backends = []

        # Setup logging
        self.log = logging.getLogger('bot_base')

        # Setup config
        self.configs = {}

        self.config = Config(path=os.path.join(data_folder, "config.toml"))
        self.config.register("data_folder", factory(config_types.Str))

        self.config.set({
            "data_folder": data_folder,
        }, no_save=True)

        self.config.load()

        self.modules = ModuleManager(self)

        self.loop = loop
        self.modules.load_modules()

    def is_ready(self):
        return False

    async def on_ready(self):
        self.info("Bot ready.")

    def dispatch(self, event, *args, **kwargs):
        """Dispatch event"""
        for module in self.modules:
            print(f"Dispatched: {event}\n{args}{kwargs}")
            module.dispatch(event, *args, **kwargs)

    async def on_error(self, event_method, *args, **kwargs):
        self.error(f"Error in {event_method}: \n{traceback.format_exc()}")

    # Logging
    def info(self, info, *args, **kwargs):
        if self.log:
            self.log.info(info, *args, **kwargs)
        self.dispatch("log_info", info, *args, **kwargs)

    def error(self, e, *args, **kwargs):
        print(e)
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

    def register(self, backend):
        self.backends.append(backend)
        backend.set_dispatch_handler(self.dispatch)

    def run(self):
        for back in self.backends:
            asyncio.ensure_future(back.run())
        self.loop.run_forever()
