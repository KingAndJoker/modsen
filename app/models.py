""" database model """
import datetime
from typing import Any

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
    Text
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class"""

    def __init__(self, **kw: Any):
        super().__init__(**kw)


# TODO: misspell
documentsRubircs = Table(
    "documents_rubrics",
    Base.metadata,
    Column("document_id", ForeignKey("documents.id", ondelete="CASCADE")),
    Column("rubric_id", ForeignKey("rubrics.id")),
)


class Rubric(Base):
    """Rubrics model"""

    __tablename__ = "rubrics"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    rubric: Mapped[str] = mapped_column(String(40))

    documents: Mapped[list["Document"]] = relationship(
        "Document", secondary=documentsRubircs, back_populates="rubrics"
    )

    def __init__(self, id: int = None, rubric: str = None, **kw: Any):
        super().__init__(**kw)
        self.id = id
        self.rubric = rubric

    def __iter__(self):
        yield "id", self.id
        yield "rubric", self.rubric


class Document(Base):
    """Document model"""

    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    text: Mapped[str] = mapped_column(Text)
    created_date: Mapped[datetime.datetime] = mapped_column(DateTime)

    rubrics: Mapped[list[Rubric]] = relationship(
        "Rubric",
        secondary=documentsRubircs,
        back_populates="documents",
        cascade="all, delete",
    )

    def __init__(
        self,
        id: int = None,
        text: str = None,
        created_date: datetime.datetime = None,
        rubrics: list[Rubric] = None,
        **kw: Any
    ):
        super().__init__(**kw)
        self.id = id
        self.text = text
        self.created_date = created_date
        self.rubrics = rubrics

    def __iter__(self):
        yield "id", self.id
        yield "text", self.text
        yield "created_date", self.created_date
        yield "rubrics", [dict(rubric) for rubric in self.rubrics]
