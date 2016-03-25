import asyncio
import aioredis


class PubSub:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sub = None
        self.pub = None

    async def connect(self):
        self.sub = await aioredis.create_redis((self.host, self.port))
        self.pub = await aioredis.create_redis((self.host, self.port))
    
    async def cleanup(self):
        self.sub.close()
        self.pub.close()
        await self.sub.wait_closed()
        await self.pub.wait_closed()

    async def get_channel(self, chan_id):
        chan, = await self.sub.subscribe(chan_id)
        return chan

    async def close_channel(self, chan):
        await self.sub.unsubscribe(chan.name)

    async def publish(self, chan_id, json_obj):
        await self.pub.publish_json(chan_id, json_obj)
