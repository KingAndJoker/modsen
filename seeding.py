""" seeding file """
import csv
import datetime
from ast import literal_eval

from environs import Env
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from app.models import Document, Rubric


def seeding(engine: Engine, path_to_csv: str = "posts.csv") -> None:
    """seeding database"""

    with Session(engine) as session:
        with open(path_to_csv, encoding="utf-8") as csv_file:
            spamreader = csv.DictReader(csv_file, delimiter=",", quotechar='"')
            for row in spamreader:
                text = row["text"]
                created = datetime.datetime.fromisoformat(row["created_date"])
                rubrics = literal_eval(row["rubrics"])
                for i, rubric in enumerate(rubrics):
                    db_rubric = (
                        session.query(Rubric)
                        .filter(Rubric.rubric == rubric)
                        .one_or_none()
                    )
                    if not db_rubric:
                        db_rubric = Rubric(rubric=rubric)
                    rubrics[i] = db_rubric

                document = Document(text=text,
                                    created_date=created,
                                    rubrics=rubrics
                                    )

                session.add(document)
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
    seeding(engine)
