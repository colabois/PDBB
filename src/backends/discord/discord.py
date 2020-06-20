import asyncio

import time

import aiohttp

from .message import Message
from ..abc import Client
from ..abc.status import Activity, Status, StatusType, ActivityType

from .intents import Intents
from .gateway import Gateway


class Discord(Client):
    def __init__(self, token, intents=Intents.DEFAULTS, loop=asyncio.get_event_loop()):
        self.token = token
        self.api_root = "https://discord.com/api"
        self.intents = intents
        self.loop = loop
        self.gateway_root = None
        self.gateway = None
        self.heartbeat_interval = None
        self.heartbeat = None
        self.dispatch = lambda *x, **y: None
        self.last_seq = 0

    async def api_call(self, path, method="GET", **kwargs):
        headers = {
            "Authorization": f"Bot {self.token}",
            "User-Agent": "Bot"
        }
        async with aiohttp.ClientSession() as session:
            async with session.request(method, self.api_root + path, headers=headers, **kwargs) as response:
                try:
                    assert 200 <= response.status < 300
                    if response.status in [200, 201]:
                        return await response.json()
                except Exception as e:
                    if response.status == 400:
                        raise Exception("Status = 400")
                    elif response.status == 403:
                        raise Exception("Status = 403")
                    else:
                        raise Exception("Chépa")

    async def get_gateway_root(self):
        return (await self.api_call("/gateway"))["url"]

    async def run(self):
        self.gateway_root = await self.get_gateway_root()
        self.gateway = Gateway(self.gateway_root, loop=self.loop)
        self.heartbeat = asyncio.create_task(self.__heartbeat())
        async for data in self.gateway.run():
            self.last_seq = data.get("s") or self.last_seq
            await self.handle_receive(data)

    async def handle_receive(self, data):
        if data.get("op") == 0:
            self.handle_event(data)
        elif data.get("op") == 1:
            await self.heartbeat_ack()
        elif data.get("op") == 10:
            self.heartbeat_interval = data.get("d", {}).get("heartbeat_interval", None)
            await self.identify()
        elif data.get("op") == 11:
            # Ping ack
            pass
        else:
            pass

    async def set_status(self, status: Status):
        await self.gateway.send({
            "op": 3,
            "d": self._to_discord_status(status)
        })

    async def identify(self):
        await self.gateway.send({
            "op": 2,
            "d": {
                "token": f"{self.token}",
                "properties": {
                    "$os": "linux",
                    "$browser": "PBA",
                    "$device": "PBA"
                },
                "large_threshold": 250,
                "guild_subscriptions": True,
                "intents": self.intents
            }
        })

    async def __heartbeat(self):
        while True:
            await asyncio.sleep((self.heartbeat_interval or 1000) / 1000)
            if not self.gateway.closed:
                await self.gateway.send({"op": 1, "d": self.last_seq})

    async def heartbeat_ack(self):
        await self.gateway.send({"op": 11})

    def handle_event(self, data):
        self.last_seq = data.get("s")
        event_name = data.get("t")
        print(f"Event: {event_name}")
        if event_name == "MESSAGE_CREATE":
            message = Message(self)
            message.from_raw_discord(data.get("d"))
            self.dispatch("message", message)

    @staticmethod
    def _to_discord_status(status):
        data = {}
        status_name = ""
        if status.status == StatusType.ONLINE:
            status_name = "online"
        elif status.status == StatusType.DO_NOT_DISTURB:
            status_name = "dnd"
        elif status.status == StatusType.IDLE:
            status_name = "idle"
        elif status.status == StatusType.INVISIBLE:
            status_name = "invisible"
        elif status.status == StatusType.OFFLINE:
            status_name = "offline"
        data.update({"status": status_name})
        data.update({"afk": status.afk})
        if status.activity:
            data.update(
                {"game": {"name": status.activity.name, "type": status.activity.type}, "since": time.time()})
        return data
