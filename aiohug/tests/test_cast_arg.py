import pytest
from marshmallow import fields, Schema

from aiohug.arguments import cast_arg


class TestSchema(Schema):
    arg = fields.Integer()


@pytest.mark.parametrize(
    "arg,annotation,casted",
    (
        ("5", fields.Integer, 5),
        ("5", fields.Integer(), 5),
        ({"arg": "5"}, TestSchema, {"arg": 5}),
        ({"arg": "5"}, TestSchema(), {"arg": 5}),
        ("5", int, 5),
    ),
)
def test_field_class(arg, annotation, casted):
    assert cast_arg(arg, annotation) == casted
