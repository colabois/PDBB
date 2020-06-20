from backends import abc


class Channel(abc.Channel):
    id: str

    async def _send(self, message):
        print(f"send: {message}")
        print(type(message))
        await self.client.send_raw(f"PRIVMSG {self.id} :{message.content}\r\n".encode())

    def from_irc_id(self, id):
        self.id = id.decode()