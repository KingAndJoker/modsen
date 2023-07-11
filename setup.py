""" setup file """
from aiohttp import web
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.models import Base
from app.api import routes as routes_api


def setup_db(app: web.Application) -> None:
    """ setup database """

    engine = create_engine("postgresql+psycopg2://modsen_practica:1@localhost:5432", echo=False)
    app['engine'] = engine
    Base.metadata.create_all(engine)

    app['session'] = Session(engine)


def setup_routes(app: web.Application) -> None:
    """ setup routes """

    app.add_routes(routes_api)


def setup(app: web.Application) -> None:
    """ setup web application """

    setup_db(app)
    setup_routes(app)
