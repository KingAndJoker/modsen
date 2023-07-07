""" database model """
import datetime

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


class Base(DeclarativeBase):
    """ Base class """

    pass


class Rubrics(Base):
    """ Rubrics model """
    __tablename__ = 'rubrics'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    document_id: Mapped[int] = mapped_column(ForeignKey('documents.id'))
    rubrics: Mapped[str] = mapped_column(String(40))


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
