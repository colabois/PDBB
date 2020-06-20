from .server import Server
from .user import User


class Message:
    server: Server
    channel = None
    author: User

    content: str
    timestamp: int

    def __init__(self, client, server=None, channel=None, author=None, content=None, timestamp=None):
        self.client = client
        self.server = server
        self.channel = channel
        self.author = author
        self.content = content
        self.timestamp = timestamp
