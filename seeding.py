""" seeding file """
import csv
import datetime
from ast import literal_eval

from environs import Env
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from app.models import Document, Rubric
from app.schema import DocumentSchema, RubricSchema
import marshmallow

def seeding_from_csv(engine: Engine, path_to_csv: str = "posts.csv") -> None:
    """seeding database"""

    document_schema = DocumentSchema()
    with Session(engine) as session:
        with open(path_to_csv, encoding="utf-8") as csv_file:
            docs_dict = csv.DictReader(csv_file, delimiter=",", quotechar='"')
            for row in docs_dict:
                doc_dict = dict(row)
                doc_dict['rubrics'] = literal_eval(doc_dict['rubrics'])
                doc_dict['rubrics'] = [{'rubric': rubric} for rubric in doc_dict['rubrics']]
                document = document_schema.load(doc_dict)

                session.add(document)

        session.commit()


def seeding_from_txt(engine: Engine, path: str = "documents.txt") -> None:
    """ seeding from txt """

    document_schema = DocumentSchema()

    with Session(engine) as session:
        with open(path, encoding="utf-8") as file:
            lists_of_doc = file.read()
            documents = document_schema.load(literal_eval(lists_of_doc), many=True)
            session.add_all(documents)

        session.commit()


if __name__ == "__main__":
    env = Env()
    env.read_env()
    url = (
        f'{env("DIALECT_DATABASE")}+{env("DRIVER_DATABASE")}://'
        f'{env("USERNAME_DATABASE")}:{env("PASSWORD_DATABASE")}@'
        f'{env("HOST_DATABASE")}:{env("PORT_DATABASE")}'
    )
    engine = create_engine(url, echo=False)
    seeding_from_csv(engine)
