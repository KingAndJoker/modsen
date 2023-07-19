""" middlewares file """
import time

from aiohttp import web


@web.middleware
async def middleware(request: web.Request, handler) -> web.Response:
    """middlewares def"""

    start_time = time.time()
    request["start_time"] = start_time
    response: web.Response = await handler(request)
    work_time = time.time() - start_time

    return response
