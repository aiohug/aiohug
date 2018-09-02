import pytest
from marshmallow import Schema, fields

from aiohug import swagger
from aiohug.swagger.decorators import ensure_swagger_attr


class TestSchema(Schema):
    field = fields.Integer()


def test_ensure_swagger_attr():
    def handler():
        pass

    with pytest.raises(AttributeError):
        handler.swagger_spec

    ensure_swagger_attr(handler)
    handler.swagger_spec == {"responses": {}}


def test_response():
    code = 201
    schema = TestSchema
    description = "test"

    @swagger.response(code, schema=schema, description=description)
    def handler():
        pass

    assert code in handler.swagger_spec["responses"]
    assert handler.swagger_spec["responses"][code]["schema"] == schema
    assert handler.swagger_spec["responses"][code]["description"] == description


def test_response_code():
    code = 201

    @swagger.response(code)
    def handler():
        pass

    assert code in handler.swagger_spec["responses"]
    assert handler.swagger_spec["responses"][code] == {}


def test_spec():
    attrs = {"private": True, "exclude": True, "deprecated": True, "tags": ["test"]}

    @swagger.spec(**attrs)
    def handler():
        pass

    for attr, value in attrs.items():
        assert handler.swagger_spec[attr] == value


def test_spec_response_codes():
    codes = [200, 409]

    @swagger.spec(response_codes=codes)
    def handler():
        pass

    assert list(handler.swagger_spec["responses"].keys()) == codes
