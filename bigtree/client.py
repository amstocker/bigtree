import asyncio
import json
from aiohttp import web
from uuid import uuid4

from . import utils


class Client:

    def __init__(self, app, ws):
        self.client_id = utils.random_id()
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
            if "action" not in json_obj:
                raise ValueError
            if "content" not in json_obj:
                raise ValueError
        except ValueError:
            return self.send_err("invalid JSON")
        
        action = json_obj["action"]
        content = json_obj["content"]
        json_obj["client_id"] = self.client_id
        
        if action == "message":
            if "channel_id" not in content:
                return self.send_err("channel ID not specified")
            else:
                chan_id = content["channel_id"]
            if chan_id not in self.channels:
                return self.send_err("client not subscribed to this channel")

            content["id"] = str(uuid4())
            content["author"] = self.client_id
            await self.pubsub.publish(chan_id, json_obj)
        
        # TODO: put timer on client_id set members?  So if server crashes the
        #       set will eventually be updated unless theres a new heartbeat.
        elif action == "heartbeat":
            channel_info = []
            for chan_id in self.channels.keys():
                channel_info.append(
                    await self.pubsub.update_info(chan_id, self.client_id)
                    )
            json_obj["content"] = channel_info
            self.ws.send_str(json.dumps(json_obj))

        elif action == "subscribe":
            if "channel_id" not in content:
                return self.send_err("channel ID not specified")
            else:
                chan_id = content["channel_id"]
            if chan_id in self.channels:
                return self.send_err("client already subscribed to this channel")
            
            task = asyncio.ensure_future(self.pubsub_reader(chan_id))
            self.channels[chan_id] = task

        else:
            return self.send_err("invalid action");


    async def pubsub_reader(self, chan_id):
        chan = await self.pubsub.get_channel(chan_id)
        try:
            async for msg in chan.iter():
                self.ws.send_str(msg.decode('utf-8'))
        except asyncio.CancelledError:
            await self.pubsub.close_channel(chan, self.client_id)
        except RuntimeError:
            return


    def send_err(self, msg):
        self.ws.send_str('{{"action": "error", "content": "{}"}}')


    async def close(self, msg):
        pass
