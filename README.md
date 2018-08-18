aiohug: 
==============================

[![build status](https://gitlab.ix/online-presence/aiohug/badges/master/build.svg)](https://gitlab.ix/online-presence/aiohug/commits/master) [![coverage report](https://gitlab.ix/online-presence/aiohug/badges/master/coverage.svg)](https://gitlab.ix/online-presence/aiohug/commits/master)

# Tasks:

- Unpack aiohttp request to arguments with annotations
- Validate handlers arguments
- Generate swagger specification


# Examples

## Run ping pong application

```python
from aiohttp import web
from aiohug import RouteTableDef

routes = RouteTableDef()


@routes.get("/ping/")
async def ping():
  return "pong"


app = web.Application()
app.add_routes(routes)


if __name__ == "__main__":
    web.run_app(app)
```

There is no more `request` object in handler.


## Arguments from path and query

```python

@routes.get("/hello/{name}/")
    async def hello(name: fields.String(), greeting: fields.String() = "Hello"):
        return {"msg": f"{greeting}, {name}"}
```


## Body with schema

```python
from aiohttp import web
from aiohug import RouteTableDef

routes = RouteTableDef()

class PayloadSchema(Schema):
    count = fields.Int()

@routes.get("/")
async def with_body(body: PayloadSchema()):
    return body

app = create_app()
app.add_routes(routes)

client = await test_client(app)
resp = await client.get("/", json={"count": "5", "another": 7})

assert await resp.json() == {"count": 5}
```

# TODO:

- don't pass default arguments
- pretty error message
