""" database model """
import datetime
from typing import Any

from sqlalchemy import (
    Text,
    Integer,
    ForeignKey,
    String,
    DateTime
)
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    """ Base class """

    def __init__(self, **kw: Any):
        super().__init__(**kw)


class Rubric(Base):
    """ Rubrics model """
    __tablename__ = 'rubrics'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    document_id: Mapped[int] = mapped_column(ForeignKey('documents.id'))
    rubric: Mapped[str] = mapped_column(String(40))

    document: Mapped['Document'] = relationship(
        'Document', back_populates='rubrics')

    def __init__(self, id: int = None,
                 document_id: int = None,
                 rubric: str = None,
                 **kw: Any):
        super().__init__(**kw)
        self.id = id
        self.document_id = document_id
        self.rubric = rubric


class Document(Base):
    """ Document model """

    __tablename__ = 'documents'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    text: Mapped[str] = mapped_column(Text)
    created_date: Mapped[datetime.datetime] = mapped_column(DateTime)

    rubrics: Mapped[list[Rubric]] = relationship(
        'Rubrics', back_populates='document')

    def __init__(self,
                 id: int = None,
                 text: str = None,
                 created_date: datetime.datetime = None,
                 rubrics: list[Rubric] = None,
                 **kw: Any):
        super().__init__(**kw)
        self.id = id
        self.text = text
        self.created_date = created_date
        self.rubrics = rubrics
