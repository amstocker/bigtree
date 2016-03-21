import asyncio
import aioredis


class PubSub:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.conn = None

    async def connect(self):
        self.conn = await aioredis.create_redis((self.host, self.port))

    async def reader(self, chan):
        pass

    async def subscribe(self, chat_id):
        pass
