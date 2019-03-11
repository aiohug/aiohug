from functools import wraps

from aiohttp import web

from aiohug import RouteTableDef


def create_app():
    app = web.Application()
    return app


def decorator(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        result = await func(*args, **kwargs)
        return f"a_{result}"

    return wrapper


async def test_decorator(aiohttp_client):
    routes = RouteTableDef()

    @routes.get("/ping/")
    @decorator
    async def hello():
        return "pong"

    app = create_app()
    app.add_routes(routes)

    client = await aiohttp_client(app)
    resp = await client.get("/ping/")
    assert resp.status == 200
    text = await resp.text()
    assert "a_pong" in text


async def test_multiple_decorators(aiohttp_client):
    routes = RouteTableDef()

    @routes.get("/ping/")
    @decorator
    @decorator
    @decorator
    async def hello():
        return "pong"

    app = create_app()
    app.add_routes(routes)

    client = await aiohttp_client(app)
    resp = await client.get("/ping/")
    assert resp.status == 200
    text = await resp.text()
    assert "a_a_a_pong" in text
