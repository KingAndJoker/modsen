""" setup file """
import os

from aiohttp import web
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from app.models import Base


def seeding(engine: Engine) -> None:
    """ sedding database """

    pass


def setup_db(app: web.Application) -> None:
    """ setup database """

    required_seeding = not os.path.isfile('./database.db')

    engine = create_engine("sqlite:///database.db", echo=False)
    app['engine'] = engine
    Base.metadata.create_all(engine)

    if required_seeding:
        seeding(engine)


def setup(app: web.Application) -> None:
    """ setup web application """

    setup_db(app)
