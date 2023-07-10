""" setup file """
import os
import csv
import datetime
from ast import literal_eval

from aiohttp import web
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.engine import Engine

from app.models import (
    Base,
    Rubric,
    Document
)
from app.api import routes as routes_api


def seeding(engine: Engine) -> None:
    """ sedding database """

    with Session(engine) as session:
        with open('posts.csv', encoding='utf-8') as csv_file:
            spamreader = csv.DictReader(csv_file, delimiter=',', quotechar='"')
            for row in spamreader:
                text = row['text']
                created = datetime.datetime.fromisoformat(row['created_date'])
                rubrics = literal_eval(row['rubrics'])
                for i, rubric in enumerate(rubrics):
                    r = session.query(Rubric). \
                        filter(Rubric.rubric == rubric). \
                        one_or_none()
                    if r is None:
                        r = Rubric(rubric=rubric)
                    rubrics[i] = r

                document = Document(
                    text=text,
                    created_date=created,
                    rubrics=rubrics
                )

                session.add(document)
                session.commit()


def setup_db(app: web.Application) -> None:
    """ setup database """

    required_seeding = not os.path.isfile('./database.db')

    engine = create_engine("sqlite:///database.db", echo=False)
    app['engine'] = engine
    Base.metadata.create_all(engine)

    if required_seeding:
        seeding(engine)

    app['session'] = Session(engine)


def setup_routes(app: web.Application) -> None:
    """ setup routes """

    app.add_routes(routes_api)


def setup(app: web.Application) -> None:
    """ setup web application """

    setup_db(app)
    setup_routes(app)
