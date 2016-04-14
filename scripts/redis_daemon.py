import asyncio
import aioredis
import time

ALL_CHANNELS_KEY = "all_channels"
HEARTBEAT_TIMEOUT = 5
UPDATE_WAIT = 1


def get_config(path):
    import json
    with open(path) as f:
        config = json.loads(f.read())
    return config


async def daemon():
    config = get_config("private/config.json")

    conn = await aioredis.create_redis((config["REDIS_HOST"],
                                        config["REDIS_PORT"]),
                                       encoding='utf-8')
    
    while True:
        start = time.time()

        all_channels = await conn.smembers(ALL_CHANNELS_KEY)
        for chan_id in all_channels:
            # remove clients who have not sent a heartbeat message in some amount
            # of seconds.
            expire = time.time() - HEARTBEAT_TIMEOUT
            await conn.zremrangebyscore(chan_id, max=expire)

        asyncio.sleep(max(UPDATE_WAIT - (time.time() - start), 0))
 
loop = asyncio.get_event_loop()
loop.run_until_complete(daemon())
loop.close()
