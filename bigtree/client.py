

class Client:
  
  def __init__(self, app, req, ws):
    self._db = app['db']
    self._req = req
    self._ws = ws
  
  async def handle(self, msg):
    ret = str(await self._db.execute("SELECT 1;"))
    self._ws.send_str(ret)
  
  async def close(self):
    pass
