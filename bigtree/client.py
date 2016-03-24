import json
import random
import string
import asyncio
from aiohttp import web


class Client:
  
    def __init__(self, app, ws):
        self.client_id = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(8))
        self.app = app
        self.ws = ws
        self.channels = {}

    async def handle(self, msg):
        if msg.tp == web.MsgType.close:
            for task in self.channels.values():
                task.cancel()
            return
            
        json_obj = json.loads(msg.data)
        action = json_obj["action"]
        chan_id = json_obj["chan_id"]

        if action == "subscribe":
            if chan_id in self.channels:
                return
            task = asyncio.ensure_future(self.pubsub_reader(chan_id))
            self.channels[chan_id] = task
        
        elif action == "message":
            if chan_id not in self.channels:
                return
            with (await self.app.pubsub.pool) as conn:
                json_obj["client_id"] = self.client_id
                await conn.publish_json(chan_id, json_obj)


    async def pubsub_reader(self, chan_id):
        with (await self.app.pubsub.pool) as conn:
            chan, = await conn.subscribe(chan_id)
            try:
                async for msg in chan.iter():
                    self.ws.send_str(msg.decode('utf-8'))
            except asyncio.CancelledError:
                await conn.unsubscribe(chan_id)


    async def close(self, msg):
        pass
