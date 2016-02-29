

class Client:
  
  def __init__(self, req, ws):
    self._req = req
    self._ws = ws
  
  async def handle(self, msg):
    self._ws.send_str("Hello, {}".format(msg.data))
  
  async def close(self):
    pass
