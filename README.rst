aiohug
======

|version| |pipeline status| |coverage report|

.. |pipeline status| image:: https://gitlab.com/nonamenix/aiohug/badges/master/pipeline.svg
   :target: https://gitlab.com/nonamenix/aiohug/commits/master
.. |coverage report| image:: https://gitlab.com/nonamenix/aiohug/badges/master/coverage.svg
   :target: https://gitlab.com/nonamenix/aiohug/commits/master
.. |version| image:: https://badge.fury.io/py/aiohug.svg
   :target: https://badge.fury.io/py/aiohug

Goals:
======

-  Unpack aiohttp (>=3.1) request to arguments with annotations
-  Validate handlers arguments
-  Generate swagger specification

Examples
========

Arguments from path and query
-----------------------------

.. code:: python

   from aiohttp import web
   from aiohug import RouteTableDef

   routes = RouteTableDef()


   @routes.get("/hello/{name}/")
   async def hello(name: fields.String(), greeting: fields.String() = "Hello"):
       return {"msg": f"{greeting}, {name}"}


   app = web.Application()
   app.add_routes(routes)


   if __name__ == "__main__":
       web.run_app(app)

There is no more ``request`` object in handler only required arguments.
   

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

Swagger
-------

Use aiohug_swagger_ package.

.. _aiohug_swagger: https://github.com/nonamenix/aiohug_swagger


Why aiohug?
===========

It's just hug_ API implementation for aiohttp 

.. _hug: https://github.com/timothycrosley/hug

TODO:
=====

-  don’t pass default arguments
