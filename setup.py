""" setup file """
from aiohttp import web
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from environs import Env

from app.models import Base
from app.api import routes as routes_api


def setup_db(app: web.Application) -> None:
    """ setup database """

    env: Env = app['env']
    url_database = f'{env("DIALECT_DATABASE")}+{env("DRIVER_DATABASE")}://' \
                   f'{env("USERNAME_DATABASE")}:{env("PASSWORD_DATABASE")}@' \
                   f'{env("HOST_DATABASE")}:{env("PORT_DATABASE")}'
    engine = create_engine(url_database, echo=False)
    app['engine'] = engine
    Base.metadata.create_all(engine)

    app['session'] = Session(engine)


def setup_routes(app: web.Application) -> None:
    """ setup routes """

    app.add_routes(routes_api)


def setup(app: web.Application) -> None:
    """ setup web application """

    env = Env()
    env.read_env()
    app['env'] = env
    setup_db(app)
    setup_routes(app)
