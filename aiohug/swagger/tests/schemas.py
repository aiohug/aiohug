from marshmallow import Schema, fields


class TestingFieldsSchema(Schema):
    integer = fields.Integer()
    float = fields.Float()
    boolean = fields.Boolean()
    datetime = fields.DateTime()
    timedelta = fields.TimeDelta()
    dictionary = fields.Dict()
    url = fields.Url()
    email = fields.Email()


class TestingSchema(Schema):
    hug_types_number = fields.Integer()
    hug_types_greater_than_5 = fields.Integer()
    hug_types_in_range_1_5 = fields.Integer()
