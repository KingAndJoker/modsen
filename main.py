""" main file """
from aiohttp import web

from setup import setup
from app.middleware import middleware


app: web.Application = web.Application(middlewares=[middleware])


if __name__ == '__main__':
    setup(app)
    web.run_app(app)
