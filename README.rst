aiohug
======

|version| |pipeline status| |coverage report|

.. |pipeline status| image:: https://gitlab.com/nonamenix/aiohug/badges/master/pipeline.svg
   :target: https://gitlab.com/nonamenix/aiohug/commits/master
.. |coverage report| image:: https://coveralls.io/repos/github/nonamenix/aiohug_swagger/badge.svg?branch=HEAD
   :target: https://coveralls.io/github/nonamenix/aiohug_swagger?branch=HEAD
.. |version| image:: https://badge.fury.io/py/aiohug.svg
   :target: https://badge.fury.io/py/aiohug

Goals:
======

-  Unpack aiohttp (>=3.1) request to arguments with annotations
-  Validate handlers arguments
-  Generate swagger specification

Posts:
======
- `Meet the aiohug`_ 

.. _`Meet the aiohug`: https://github.com/nonamenix/notes/blob/master/notes/20190309_aiohug.md

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

There is no ``request`` object in handler signature anymore - only required arguments.
   

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


Decorators
----------

Because of the way ``aiohttp`` routing works all decorators to resource handlers
must be applied **BEFORE** ``aiohug``'s routing decorator, i.e.

.. code:: python

   def some_decorator(func):

    @wraps(func)
    def wrapper(request, *args, **kwargs):
        # Some logic for decorator
        return func(*args, **kwargs)

    return wrapper


    @routes.get("/ping/")
    @some_decorator
    async def hello():
        return "pong"


Moreover, make sure to decorate wrapper functions with ``wraps`` decorator from ``functools`` module
- otherwise ``aiohug`` won't be able to access original handler's arguments and annotations.



Why aiohug?
===========

It's just hug_ API implementation for ``aiohttp``

.. _hug: https://github.com/timothycrosley/hug

TODO:
=====

-  don’t pass default arguments
