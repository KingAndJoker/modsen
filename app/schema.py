""" Schema file """
from marshmallow import Schema, fields, post_load

from app.models import Document, Rubric


class RubricSchema(Schema):
    """Rubric schema"""

    class Meta:
        model = Rubric
        fields = ("id", "rubric")

    id = fields.Int(allow_none=True)
    rubric = fields.Str()

    @post_load
    def make_rubric(self, data, **kwargs):
        """ return Rubric object """

        return Rubric(**data)


class DocumentSchema(Schema):
    """Document schema"""

    class Meta:
        model = Document
        fields = ("id", "text", "created_date", "rubrics")
        ordered = True

    id = fields.Int(allow_none=True)
    text = fields.Str()
    created_date = fields.DateTime()
    rubrics = fields.List(fields.Nested(RubricSchema()))

    @post_load
    def make_document(self, data, **kwargs):
        """ return Document object """

        return Document(**data)
