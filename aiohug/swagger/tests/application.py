from aiohttp import web
from aiohug import swagger, RouteTableDef
from marshmallow import Schema, fields


class TestingFieldsSchema(Schema):
    integer = fields.Integer()
    float = fields.Float()
    boolean = fields.Boolean()
    datetime = fields.DateTime()
    timedelta = fields.TimeDelta()
    dictionary = fields.Dict()
    url = fields.Url()
    email = fields.Email()


class TestingSchema(Schema):
    hug_types_number = fields.Integer()
    hug_types_greater_than_5 = fields.Integer()
    hug_types_in_range_1_5 = fields.Integer()


routes = RouteTableDef()


@routes.get("/hello/{name}/")
async def hello(name: fields.String(), greeting: fields.String() = "Hello"):
    return {"msg": f"{greeting}, {name}"}


@routes.get("/swagger/hug/{hug_types_number}/{hug_types_greater_than_5}/")
async def openapi_test(request, hug_timer, hug_types_number: fields.Number()):
    """Endpoint with hug.types

    Not versioned api method"""
    return {"hug_types_number": hug_types_number}


@routes.get("/swagger/marshmallow/{swagger_types_number}/", versions=[2, 3])
@swagger.response(200, description="Good response", schema=TestingSchema)
@swagger.response(400, description="Bad response")
async def openapi_test_swagger_types(
    request,
    hug_timer,
    swagger_types_number: fields.Integer(),
    swagger_types_number_in_query: fields.Integer() = 3,
) -> TestingSchema():
    """Endpoint with marshmallow types"""
    return {
        "swagger_types_number": swagger_types_number,
        "swagger_types_number_in_query": swagger_types_number_in_query,
    }


@routes.post("/swagger/marshmallow/post-body")  # TODO: check with last slash
@swagger.response(201, description="Created", schema=TestingSchema())
async def openapi_post_body(body: TestingSchema()) -> TestingSchema():
    return body


app = web.Application()
app.add_routes(routes)
