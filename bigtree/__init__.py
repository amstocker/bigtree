import asyncio
from .server import Server

app = Server()
loop = asyncio.get_event_loop()
loop.run_until_complete(app.init())
