#!/usr/bin/python3
import asyncio
import json
import logging
import os

from bot_base.bot_base import BotBase


def setup_logging(default_path='data/log_config.json', default_level=logging.INFO, env_key='BOT_BASE_LOG_CONFIG'):
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
    print(os.environ.get("LOCAL_MODULES", "modules"))
    client = BotBase(max_messages=500000, data_folder="datas")

    async def start_bot():
        await client.start(os.environ.get("DISCORD_TOKEN"))

    loop = asyncio.get_event_loop()
    loop.create_task(start_bot())
    loop.run_forever()


if __name__ == "__main__":
    main()
