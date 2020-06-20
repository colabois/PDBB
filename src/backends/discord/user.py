from .. import abc


class User(abc.User):
    id: int
    bot: bool
    discriminator: str

    def from_discord_raw(self, data):
        self.id = data.get("id")
        self.bot = data.get("bot")
        self.discriminator = data.get("discriminator")
