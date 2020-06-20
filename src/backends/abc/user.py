class User:
    bot: bool = False

    def __init__(self, client):
        self.client = client
