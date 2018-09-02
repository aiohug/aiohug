import pytest

from aiohttp import web
from aiohug import RouteTableDef
from ..handlers import routes as swagger_handlers


@pytest.fixture
def app() -> web.Application:
    routes = RouteTableDef()

    @routes.get("/")
    async def ping():
        return "pong"

    app = web.Application()
    app.add_routes(routes)
    app.add_routes(swagger_handlers)
    return app


async def test_swagger_json(app, test_client):
    client = await test_client(app)
    resp = await client.get("/swagger.json")
    body = await resp.json()
    assert resp.status == 200
    assert resp.content_type == "application/json"

    # assert body == {}


async def test_swagger_yaml(app, test_client):
    client = await test_client(app)
    resp = await client.get("/swagger.yaml")
    assert resp.status == 200
    assert resp.content_type == "text/yaml"
    text = await resp.text()

    # assert text == ''


async def test_swagger(app, test_client):
    client = await test_client(app)
    resp = await client.get("/swagger/")
    assert resp.status == 200
    assert resp.content_type == "text/html"

    # text = await resp.text()
