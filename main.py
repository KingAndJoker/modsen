""" main file """
from aiohttp import web

from setup import setup


app: web.Application = web.Application()


if __name__ == '__main__':
    setup(app)
    web.run_app(app)
