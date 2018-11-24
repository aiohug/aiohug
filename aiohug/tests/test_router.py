from aiohttp import web
from marshmallow import fields, Schema
from aiohug import RouteTableDef


def create_app():
    app = web.Application()
    return app


async def test_ping(test_client):
    routes = RouteTableDef()

    @routes.get("/ping/")
    async def hello():
        return "pong"

    app = create_app()
    app.add_routes(routes)

    client = await test_client(app)
    resp = await client.get("/ping/")
    assert resp.status == 200
    text = await resp.text()
    assert "pong" in text


async def test_ping_with_request(test_client):
    routes = RouteTableDef()

    @routes.get("/ping/")
    async def ping(request):
        return "pong"

    app = create_app()
    app.add_routes(routes)

    client = await test_client(app)
    resp = await client.get("/ping/")
    assert resp.status == 200
    text = await resp.text()
    assert "pong" in text


async def test_hello(test_client):
    routes = RouteTableDef()

    @routes.get("/hello/{name}/")
    async def hello(name: fields.String(), greeting: fields.String() = "Hello"):
        return {"msg": f"{greeting}, {name}"}

    app = create_app()
    app.add_routes(routes)

    client = await test_client(app)
    resp = await client.get("/hello/Lucy/")
    assert resp.status == 200
    assert {"msg": "Hello, Lucy"} == await resp.json()


async def test_json_body(test_client):
    routes = RouteTableDef()

    @routes.get("/")
    async def with_body(body):
        return body

    app = create_app()
    app.add_routes(routes)

    client = await test_client(app)
    payload = {"msg": "Hello, Lucy"}
    resp = await client.get("/", json=payload)
    assert resp.status == 200
    assert await resp.json() == payload


async def test_json_body_with_schema_class(test_client):
    routes = RouteTableDef()

    class RequestSchema(Schema):
        count = fields.Int()

    @routes.get("/")
    async def with_body(body: RequestSchema):
        return body

    app = create_app()
    app.add_routes(routes)

    client = await test_client(app)
    resp = await client.get("/", json={"count": "5"})
    assert resp.status == 200
    assert await resp.json() == {"count": 5}


async def test_json_body_with_schema_instance(test_client):
    routes = RouteTableDef()

    class RequestSchema(Schema):
        count = fields.Int()

    @routes.get("/")
    async def with_body(body: RequestSchema()):
        return body

    app = create_app()
    app.add_routes(routes)

    client = await test_client(app)
    resp = await client.get("/", json={"count": "5"})
    assert resp.status == 200
    assert await resp.json() == {"count": 5}


# async def test_json_body_with_wrong_mime_type():
#     assert False
#
#     # todo: send no json mime type


async def test_cast(test_client):
    routes = RouteTableDef()

    @routes.get("/number/{number}/")
    async def return_number(number: fields.Int()):
        return {"number": number}

    app = create_app()
    app.add_routes(routes)

    client = await test_client(app)
    number = 5
    resp = await client.get(f"/number/{number}/")
    assert resp.status == 200
    assert await resp.json() == {"number": number}


async def test_cast_error(test_client):
    routes = RouteTableDef()

    @routes.get("/number/{number}/")
    async def return_number(number: fields.URL()):
        return {"number": number}

    app = create_app()
    app.add_routes(routes)

    client = await test_client(app)
    number = 5
    resp = await client.get(f"/number/{number}/")
    assert resp.status == 409
    assert await resp.json() == {
        "data": {"number": ["Not a valid URL."]},
        "status": "error",
    }


async def test_variable_not_provided_with_base_types(test_client):
    routes = RouteTableDef()

    @routes.get("/")
    async def return_number(number: int):
        return {"number": number}

    app = create_app()
    app.add_routes(routes)

    client = await test_client(app)
    resp = await client.get('/')
    assert resp.status == 409
    assert await resp.json() == {
        "data": {"number": ["Required argument"]},
        "status": "error",
    }


