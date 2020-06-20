import asyncio

from backends.IRC.message import Message
from backends.abc.client import Client


class IRCHandler(asyncio.Protocol):
    def __init__(self, client):
        self.transport = None
        self.client = client

    def connection_made(self, transport):
        self.transport = transport
        self.login()

    def data_received(self, data):
        print(data.decode())
        if data.startswith(b"PING"):
            self.transport.write(b"data".replace(b"PING", b"PONG"))
        if b"PRIVMSG" in data:
            message = Message(self.client)
            message.from_irc(data)
            self.client.dispatch("message", message)

    def eof_received(self):
        pass

    def login(self):
        self.transport.write(f"USER bot 0 * :BOTOX\r\n".encode())
        self.transport.write(f"NICK {self.client.nick}\r\n".encode())
        self.transport.write(f"JOIN #general\r\n".encode())

    def send(self, data):
        print(data)
        self.transport.write(data)


class IRC(Client):
    def __init__(self, server, port, password=None, nick="I_AM_A_BOT", user=None, mode=None, unused=None, realname=None, loop=asyncio.get_event_loop()):
        self.server = server
        self.port = port
        self.password = password
        self.nick = nick
        self.connection_handler = IRCHandler(self)
        self.loop = loop

    async def run(self, loop=asyncio.get_event_loop()):
        await loop.create_connection(lambda: self.connection_handler, self.server, self.port)

    async def send_raw(self, data):
        self.loop.run_in_executor(None, lambda: self.connection_handler.send(data))