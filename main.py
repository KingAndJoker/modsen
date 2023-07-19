""" main file """
from aiohttp import web

from app.middleware import middleware
from setup import setup

app: web.Application = web.Application(middlewares=[middleware])


if __name__ == "__main__":
    setup(app)
    web.run_app(app)
