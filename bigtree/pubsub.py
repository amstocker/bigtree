import asyncio
import aioredis
import time


class PubSub:

    HEARTBEAT_TIMEOUT = 5  # seconds

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

    async def get_channel(self, chan_id):
        chan, = await self.sub.subscribe(chan_id)
        return chan

    async def close_channel(self, chan, client_id):
        await self.info.zrem(chan_id, client_id)
        await self.sub.unsubscribe(chan.name)

    async def publish(self, chan_id, json_obj):
        await self.pub.publish_json(chan_id, json_obj)

    async def update_info(self, chan_id, client_id):
        now = time.time()
        # remove clients who have not sent a heartbeat message in some amount
        # of seconds.
        # TODO: this should really be done in a separate daemon but this is
        #       okay for now...
        expire = now - self.HEARTBEAT_TIMEOUT
        await self.info.zremrangebyscore(chan_id, max=expire)
        
        # update last score with time now
        await self.info.zadd(chan_id, now, client_id)
        
        # get current members
        members = await self.info.zrange(chan_id)
        return {
            "channel_id": chan_id,
            "members": members
            }
