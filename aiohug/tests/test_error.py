from aiohttp import web
from marshmallow import fields, Schema

from aiohug import RouteTableDef


def create_app():
    app = web.Application()
    return app


async def test_not_valid_field(test_client):
    routes = RouteTableDef()

    @routes.get("/number/{number}/")
    async def return_number(number: fields.Int()):
        return {"number": number}

    app = create_app()
    app.add_routes(routes)

    client = await test_client(app)
    resp = await client.get(f"/number/notanumber/")
    assert resp.status == 409
    assert await resp.json() == {
        "data": {"number": ["Not a valid integer."]},
        "status": "error",
    }


async def test_not_valid_schema(test_client):
    routes = RouteTableDef()

    class RequestSchema(Schema):
        a = fields.Int()
        b = fields.Int()

    @routes.get("/")
    async def with_body(body: RequestSchema):
        return body

    app = create_app()
    app.add_routes(routes)
    client = await test_client(app)
    resp = await client.get("/", json={"a": "5", "b": "c"})
    assert resp.status == 409
    assert await resp.json() == {
        "data": {"body": {"b": ["Not a valid integer."]}},
        "status": "error",
    }
