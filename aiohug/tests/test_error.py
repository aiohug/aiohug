import pytest
from aiohttp import web
from marshmallow import fields, Schema, validate

from aiohug import RouteTableDef


def create_app():
    app = web.Application()
    return app


async def test_not_valid_field(aiohttp_client):
    routes = RouteTableDef()

    @routes.get("/number/{number}/")
    async def return_number(number: fields.Int()):
        return {"number": number}

    app = create_app()
    app.add_routes(routes)

    client = await aiohttp_client(app)
    resp = await client.get("/number/notanumber/")
    assert resp.status == 409
    assert await resp.json() == {"data": {"number": ["Not a valid integer."]}, "status": "error"}


class RequestSchema(Schema):
    a = fields.Int()
    b = fields.Int()


class RequestSchemaWithRequiredFields(Schema):
    a = fields.Int()
    b = fields.Int(required=True)


class RequestSchemaWithFieldsValidation(Schema):
    a = fields.String(validate=validate.Length(min=50))


@pytest.mark.parametrize(
    "schema_class,json_data,excepted_error",
    [
        (RequestSchema, {"a": "5", "b": "c"}, {"b": ["Not a valid integer."]}),
        (RequestSchemaWithRequiredFields, {"a": "4"}, {"b": ["Missing data for required field."]}),
        (RequestSchemaWithFieldsValidation, {"a": "Too short string"}, {'a': ['Shorter than minimum length 50.']}),
    ],
)
async def test_not_valid_schema(schema_class, json_data, excepted_error, aiohttp_client):
    routes = RouteTableDef()

    @routes.get("/")
    async def with_body(body: schema_class):
        return body

    app = create_app()
    app.add_routes(routes)
    client = await aiohttp_client(app)
    resp = await client.get("/", json=json_data)
    assert resp.status == 409
    assert await resp.json() == {"data": {"body": excepted_error}, "status": "error"}
