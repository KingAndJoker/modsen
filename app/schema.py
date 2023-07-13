""" Schema file """
from marshmallow import Schema, fields


class RubricSchema(Schema):
    """ Rubric schema """

    id = fields.Int()
    rubric = fields.Str()


class DocumentSchema(Schema):
    """ Document schema """

    id = fields.Int()
    text = fields.Str()
    created_date = fields.DateTime()
    rubric = fields.Nested(RubricSchema, many=True)
