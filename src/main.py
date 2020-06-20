#!/usr/bin/python3
import asyncio
import json
import logging
import os

from backends.IRC.irc import IRC
from backends.discord.discord import Discord
from bot_base.bot_base import BotBase


def setup_logging(default_path='datas/log_config.json', default_level=logging.INFO, env_key='BOT_BASE_LOG_CONFIG'):
    """Setup logging configuration
    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


def main():
    setup_logging()
    client = BotBase()
    client.register(Discord("NDcwNzI4NjAzMDEzNzQyNjAy.XuSCkg.8A6DEqpDj9pghFDefp9PEHlASnc"))
    client.register(IRC("192.168.0.1", 6667, "toto"))
    client.run()


if __name__ == "__main__":
    main()
