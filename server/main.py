import asyncio
from aiohttp import web

from .client import Client
from .db import Database


async def init(app):
    app['db'] = Database(open('private/pg_dsn').read())
    await app['db'].connect()

async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(body=text.encode('utf-8'))

async def wshandler(req):
    ws = web.WebSocketResponse()
    await ws.prepare(req)
    
    client = Client(app, req, ws)
    async for msg in ws:
        if msg.tp == web.MsgType.text:
            await client.handle(msg)
        elif msg.tp == web.MsgType.close:
            await client.close(msg)
            break
        else:
            # invalid message type
            break

    return ws


## INIT ##
app = web.Application()
app.router.add_route('GET', '/ws/echo', wshandler)
app.router.add_route('GET', '/api/{name}', handle)

loop = asyncio.get_event_loop()
loop.run_until_complete(init(app))
