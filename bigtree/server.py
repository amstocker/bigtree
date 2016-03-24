import asyncio
from aiohttp import web

from .client import Client
from .db import Database
from .pubsub import PubSub


class Server(web.Application):

    async def init(self):
        self.router.add_route('GET', '/ws/echo', self.my_websocket_handler)

        self.database = Database(open('private/pg_dsn').read())
        self.pubsub = PubSub('localhost', 6379)
        
        await self.database.connect()
        await self.pubsub.connect()
        self.on_shutdown.append(self.my_cleanup)

    async def my_cleanup(self, app):
        await self.database.cleanup()
        await self.pubsub.cleanup()

    async def my_websocket_handler(self, req):
        ws = web.WebSocketResponse()
        await ws.prepare(req)
        
        # receiving from websocket must be
        # done in this coroutine.
        client = Client(self, ws)
        async for msg in ws:
            await client.handle(msg)

        return ws
