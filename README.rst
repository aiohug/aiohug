aiohug
======

|pipeline status| |coverage report|

.. |pipeline status| image:: https://gitlab.com/nonamenix/aiohug/badges/master/pipeline.svg
   :target: https://gitlab.com/nonamenix/aiohug/commits/master
.. |coverage report| image:: https://gitlab.com/nonamenix/aiohug/badges/master/coverage.svg
   :target: https://gitlab.com/nonamenix/aiohug/commits/master

Tasks:
======

-  Unpack aiohttp request to arguments with annotations
-  Validate handlers arguments
-  Generate swagger specification

Examples
========

Run ping pong application
-------------------------

.. code:: python

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

There is no more ``request`` object in handler.

Arguments from path and query
-----------------------------

.. code:: python


   @routes.get("/hello/{name}/")
   async def hello(name: fields.String(), greeting: fields.String() = "Hello"):
       return {"msg": f"{greeting}, {name}"}

Body with schema
----------------

.. code:: python

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

Another shortcuts
-----------------

.. code:: python 

   @routes.post("/ping/")
   async def ping():
     return 201, "pong"


Why aiohug?
===========

It's just hug_ API implementation for aiohttp 

.. _hug: https://github.com/timothycrosley/hug

TODO:
=====

-  don’t pass default arguments
-  default websocket handler with ping/pong and schemas support

.. code:: python

   ws = aiohug.WSHandler()


   @ws("hello")  # match message by `type` field
   async def hello(name: str, greeting: str="Hi"):
       """ Just send {"type": "hello", "name": "Lucy", "greeting": "Hi"} """
       return {"text", f"{greeting}, {name}"}


   app = create_app()
   app.add_routes([web.get('/ws', ws)])
