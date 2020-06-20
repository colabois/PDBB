import json

import aiohttp

from .. import abc


class Channel(abc.Channel):
    filled: bool = False
    id: int
    populated: bool

    def from_discord_id(self, id_):
        self.id = id_
        self.populated = False

    async def _send(self, message):
        form = aiohttp.FormData()
        form.add_field('payload_json', json.dumps({"content": message.content}))
        await self.client.api_call(f"/channels/{self.id}/messages", method="POST", data=form)
