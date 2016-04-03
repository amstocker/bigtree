import asyncio
import aioredis


class PubSub:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sub = None
        self.pub = None
        self.info = None

    async def connect(self):
        self.sub = await aioredis.create_redis((self.host, self.port), encoding='utf-8')
        self.pub = await aioredis.create_redis((self.host, self.port), encoding='utf-8')
        self.info = await aioredis.create_redis((self.host, self.port), encoding='utf-8')
    
    async def cleanup(self):
        self.sub.close()
        self.pub.close()
        self.info.close()
        await self.sub.wait_closed()
        await self.pub.wait_closed()
        await self.info.wait_closed()

    async def get_channel(self, chan_id, client_id):
        await self.info.sadd(chan_id, client_id)
        chan, = await self.sub.subscribe(chan_id)
        return chan

    async def close_channel(self, chan, client_id):
        await self.indo.srem(chan_id, client_id)
        await self.sub.unsubscribe(chan.name)

    async def publish(self, chan_id, json_obj):
        await self.pub.publish_json(chan_id, json_obj)

    async def get_channel_info(self, chan_id):
        members = await self.info.smembers(chan_id)
        return {
            "members": members
            }
