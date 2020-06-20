from backends.abc.status import Status


class Client:
    async def run(self):
        pass

    async def set_status(self, status: Status):
        pass

    def set_dispatch_handler(self, handler):
        self.dispatch = handler
