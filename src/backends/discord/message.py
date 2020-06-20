from pprint import pprint

from .channel import Channel
from .user import User
from .. import abc


class Message(abc.Message):
    populated: bool = False
    id: int
    tts: bool
    mention_everyone: bool
    mentions: list
    mention_roles: list
    mention_channels: list
    attachments: list
    embeds: list
    reactions: list
    nonce: list
    pinned: bool
    webhook_id: int
    type: int
    activity: int
    application: int
    message_reference: int
    flags: int

    def from_raw_discord(self, data):
        self.id = data.get("id")
        self.author = User(self.client)
        self.author.from_discord_raw(data.get("author"))
        self.channel = Channel(self.client)
        self.channel.from_discord_id(data.get("channel_id"))
        self.content = data.get("content")
        self.timestamp = data.get("timestamp")
        self.tts = data.get("tts")
        self.mention_everyone = data.get("mention_everyone")
        self.mentions = data.get("mentions")
        self.mention_roles = data.get("mention_roles")
        self.mention_channels = data.get("mention_channels")
        self.attachments = data.get("attachments")
        self.embeds = data.get("embeds")
        self.reactions = data.get("reactions")
        self.nonce = data.get("nonce")
        self.pinned = data.get("pinned")
        self.webhook_id = data.get("webhook_id")
        self.type = data.get("type")
        self.activity = data.get("activity")
        self.application = data.get("application")
        self.message_reference = data.get("message_reference")
        self.flags = data.get("flags")
        self.populated = True