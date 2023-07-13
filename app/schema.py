""" Schema file """
from marshmallow import Schema, fields

from app.models import (
    Rubric,
    Document
)


class RubricSchema(Schema):
    """ Rubric schema """

    class Meta:
        model = Rubric
        fields = ('id', 'rubric')

    id = fields.Int()
    rubric = fields.Str()


class DocumentSchema(Schema):
    """ Document schema """

    class Meta:
        model = Document
        fields = ('id', 'text', 'created_date', 'rubrics')
        ordered = True

    id = fields.Int()
    text = fields.Str()
    created_date = fields.DateTime()
    rubrics = fields.Nested(RubricSchema(), many=True)
