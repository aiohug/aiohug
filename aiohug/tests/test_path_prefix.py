import pytest
from aiohttp import web
from aiohug import RouteTableDef


def create_app():
    app = web.Application()
    return app


@pytest.mark.parametrize(
    "prefix,url",
    [
        ("prefix", "/prefix/ping/"),
        ("prefix/", "/prefix/ping/"),
        ("/prefix", "/prefix/ping/"),
        ("/prefix/", "/prefix/ping/"),
        ("/pre/fix/", "/pre/fix/ping/"),
        ("pre/fix/", "/pre/fix/ping/"),
    ],
)
async def test_ping(aiohttp_client, prefix, url):
    routes = RouteTableDef(prefix=prefix)

    @routes.get("/ping/")
    async def hello():
        return "pong"

    app = create_app()
    app.add_routes(routes)

    client = await aiohttp_client(app)
    resp = await client.get(url)
    assert resp.status == 200
    text = await resp.text()
    assert "pong" in text
