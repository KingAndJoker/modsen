""" setup file """
from aiohttp import web
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from app.models import Base


def seeding(engine: Engine) -> None:
    """ sedding database """

    pass


def setup_db(app: web.Application) -> None:
    """ setup database """

    engine = create_engine("sqlite:///database.db", echo=False)
    app['engine'] = engine
    Base.metadata.create_all(engine)


def setup(app: web.Application) -> None:
    """ setup web application """

    setup_db(app)
