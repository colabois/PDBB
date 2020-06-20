from backends.abc import Message


class Channel:
    def __init__(self, client):
        self.client = client

    async def send(self, message):
        if type(message) == str:
            await self._send(Message(self.client, content=message))
            return
        await self._send(message)

    async def _send(self, message):
        pass
