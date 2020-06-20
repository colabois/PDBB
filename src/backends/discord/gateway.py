import asyncio
import json
import traceback

import websockets


class Gateway:
    websocket: websockets.WebSocketClientProtocol

    def __init__(self, root, version=6, encoding="json", loop=asyncio.get_event_loop()):
        self.root = root
        self.version = version
        self.encoding = encoding
        self.loop = loop
        self.websocket = None

    @property
    def url(self):
        return f"{self.root}?v={self.version}&encoding={self.encoding}"

    async def run(self):
        self.websocket = await websockets.connect(self.url)
        while True:
            message = await self.websocket.recv()
            data = json.loads(message)
            yield data

    async def send(self, content):
        try:
            if self.websocket is not None:
                await self.websocket.send(json.dumps(content))
        except Exception:
            traceback.print_exc()

    @property
    def closed(self):
        return self.websocket.closed
