from backends.abc import Message


class Messagable:
    async def send(self, message: Message):
        pass