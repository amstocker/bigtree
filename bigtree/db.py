import asyncio
import aiopg


class Database:

    ## Queries
    GET_TOP_QUERY = "SELECT post FROM posts ORDER BY score(post) LIMIT %s;"
    GET_TOP_LIMIT = 50
    GET_SUBTREE_QUERY = "SELECT post FROM subtree(%s, %s);"
    GET_SUBTREE_MAX_DEPTH = 5

    def __init__(self, dsn):
        self._dsn = dsn
        self._pool = None

    async def connect(self):
        self._pool = await aiopg.create_pool(self._dsn)

    async def execute(self, cmd, *args):
        async with self._pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(cmd, args)
                return await cur.fetchall()
    
    async def add_message(self, msg):
        pass

    async def get_subtree(self, root_uuid):
        pass

    async def get_top_page(self):
        """
        Get top N threads.
        """
        return await self.execute(GET_TOP_QUERY, GET_TOP_LIMIT)

    async def spawn_updater(self, child_uuid):
        pass
