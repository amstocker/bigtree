import asyncio
import aioredis


class PubSub:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.pool = None

    async def connect(self):
        self.pool = await aioredis.create_pool((self.host, self.port))

    async def close(self):
        pass

    async def get_channel(self, chan_id):
        pass

    async def publish(self, chan_id, json_obj):
        pass
