

class Client:
  
  def __init__(self, server, ws):
    self.server = server
    self.ws = ws
  
  async def handle(self, msg):
    ret = str(await self.server.database.execute("SELECT 1;"))
    self.ws.send_str(ret)
  
  async def close(self, msg):
    pass
