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


def seeding(engine: Engine) -> None:
    """ sedding database """
    
    with Session(engine) as session:
        with open('posts.csv', encoding='utf-8') as csv_file:
            spamreader = csv.DictReader(csv_file, delimiter=',', quotechar='"')
            for row in spamreader:
                text = row['text']
                created = datetime.datetime.fromisoformat(row['created_date'])
                rubrics = literal_eval(row['rubrics'])
                rubrics = [Rubric(rubric=rubric) for rubric in rubrics]

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


def setup(app: web.Application) -> None:
    """ setup web application """

    setup_db(app)
