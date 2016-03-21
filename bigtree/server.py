import asyncio
from aiohttp import web

from .client import Client
from .db import Database
from .pubsub import PubSub


class Server(web.Application):

    async def init(self):
        self.router.add_route('GET', '/ws/echo', self.websocket_handler)

        self.database = Database(open('private/pg_dsn').read())
        self.pubsub = PubSub('localhost', 6379)
        
        await self.database.connect()
        await self.pubsub.connect()

    async def websocket_handler(self, req):
        ws = web.WebSocketResponse()
        await ws.prepare(req)

        client = Client(self, ws)
        async for msg in ws:
            if msg.tp == web.MsgType.close:
                await client.close(msg)
                break
            else:
                await client.handle(msg)

        return ws
