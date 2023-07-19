""" setup file """
from aiohttp import web
from environs import Env
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.api import routes as routes_api
from app.models import Base
from app.schema import DocumentSchema


def setup_db(
    app: web.Application, echo: bool = False
) -> None:
    """setup database"""

    env: Env = app["env"]
    DIALECT_DATABASE = env("DIALECT_DATABASE")
    DRIVER_DATABASE = env("DRIVER_DATABASE")
    USERNAME_DATABASE = env("USERNAME_DATABASE")
    PASSWORD_DATABASE = env("PASSWORD_DATABASE")
    HOST_DATABASE = env("HOST_DATABASE")
    PORT_DATABASE = env("PORT_DATABASE")

    url_database = f'{DIALECT_DATABASE}'
    url_database += f'+{DRIVER_DATABASE}' if DRIVER_DATABASE else ''
    url_database += '://'
    url_database += (
        f'{USERNAME_DATABASE}:{PASSWORD_DATABASE}@'
        if USERNAME_DATABASE and PASSWORD_DATABASE
        else ''
    )
    url_database += (
        f'{HOST_DATABASE}:{PORT_DATABASE}'
        if HOST_DATABASE and PORT_DATABASE
        else ''
    )

    engine = create_engine(url_database, echo=echo)
    app["engine"] = engine
    Base.metadata.create_all(engine)

    app["session"] = Session(engine)


def setup_routes(app: web.Application) -> None:
    """setup routes"""

    app.add_routes(routes_api)


def setup_schema(app) -> None:
    """setup schema"""

    document_schema = DocumentSchema()
    app["document_schema"] = document_schema


def setup(app: web.Application, env: Env=None, **kw) -> None:
    """setup web application"""

    if env is None:
        env = Env()
        env.read_env()

    app["env"] = env
    setup_db(app, **kw)
    setup_routes(app)
    setup_schema(app)
