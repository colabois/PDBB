from backends import abc
from backends.IRC.channel import Channel
from backends.abc import User


class Message(abc.Message):
    def from_irc(self,data):
        # :Fomys!~fomys@192.168.0.14 PRIVMSG #general :Pouet
        message = data.split(b":")[-1]
        self.content = message.decode()
        channel = data.split(b" ")[2]
        print(channel)
        if channel.decode() == self.client.nick:
            channel = data.split(b" ")[0][1:].split(b"!")[0]
        self.channel = Channel(self.client)
        self.channel.from_irc_id(channel)
        self.author = User(self.client)

