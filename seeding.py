""" seeding file """
import os
import csv
import datetime
from ast import literal_eval

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.engine import Engine

from app.models import (
    Base,
    Rubric,
    Document
)

def seeding(engine: Engine) -> None:
    """ seeding database """

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


if __name__ == '__main__':
    engine = create_engine("postgresql+psycopg2://modsen_practica:1@localhost:5432", echo=False)
    seeding(engine)