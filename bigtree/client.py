import asyncio
import json
from aiohttp import web
from uuid import uuid4

from . import utils


class Client:

    def __init__(self, app, ws):
        self.session_id = utils.random_id()
        self.app = app
        self.pubsub = app.pubsub
        self.ws = ws
        self.channels = {}

    async def handle(self, msg):
        if msg.tp == web.MsgType.close:
            for task in self.channels.values():
                task.cancel()
            return
        try:
            json_obj = json.loads(msg.data)
        except ValueError:
            return self.send_err("invalid JSON")
        action = json_obj["action"]
        chan_id = json_obj["chan_id"]
        
        if action == "subscribe":
            if chan_id in self.channels:
                return self.send_err("client already subscribed to this channel")
            task = asyncio.ensure_future(self.pubsub_reader(chan_id))
            self.channels[chan_id] = task
        
        elif action == "message":
            if chan_id not in self.channels:
                return self.send_err("client not subscribed to this channel")
            json_obj["session_id"] = self.session_id
            json_obj["content"]["id"] = str(uuid4())
            await self.pubsub.publish(chan_id, json_obj)
        
        # TODO: should be "heartbeat", put timer on client_id set members?
        elif action == "getinfo":
            if chan_id not in self.channels:
                return self.send_err("client not subscribe to this channel")
            json_obj["content"] = await self.pubsub.get_channel_info(chan_id)
            self.ws.send_str(json.dumps(json_obj))


    async def pubsub_reader(self, chan_id):
        # TODO: change this to pass in unique authenticated client ID
        chan = await self.pubsub.get_channel(chan_id, self.session_id)
        try:
            async for msg in chan.iter():
                self.ws.send_str(msg.decode('utf-8'))
        except asyncio.CancelledError:
            await self.pubsub.close_channel(chan, self.session_id)
        except RuntimeError:
            return


    def send_err(self, msg):
        self.ws.send_str('{{"error":"{}"}}')


    async def close(self, msg):
        pass
