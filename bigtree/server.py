import asyncio
from aiohttp import web

from .client import Client
from .db import Database
from .pubsub import PubSub


class Server(web.Application):

    async def init_resources(self):
        self.router.add_route('GET', '/ws/main', self.ws_main_handler)
        self.on_shutdown.append(self.cleanup_resources)

        self.database = Database(open('private/pg_dsn').read())
        self.pubsub = PubSub('localhost', 6379)
        await self.database.connect()
        await self.pubsub.connect()

    async def cleanup_resources(self, app):
        await self.database.cleanup()
        await self.pubsub.cleanup()

    async def ws_main_handler(self, req):
        ws = web.WebSocketResponse()
        await ws.prepare(req)
        
        # receiving from websocket must be
        # done in this coroutine.
        client = Client(self, ws)
        async for msg in ws:
            await client.handle(msg)

        return ws
