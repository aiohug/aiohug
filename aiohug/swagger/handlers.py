import os
import yaml
from aiohttp import web

from aiohug import RouteTableDef
from aiohug import swagger

routes = RouteTableDef()


@swagger.spec(exclude=True)
@routes.get("/swagger.json")
async def swagger_json(request):
    return swagger.generate_swagger(request.app)


@swagger.spec(exclude=True)
@routes.get("/swagger.yaml")
async def swagger_yaml(request):
    return web.Response(
        text=yaml.dump(swagger.generate_swagger(request.app)), content_type="text/yaml"
    )


@swagger.spec(exclude=True)
@routes.get("/swagger/", name="swagger")
async def root():
    template_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "templates", "index.html"
    )

    with open(template_path) as template:
        return web.Response(
            text=template.read().replace("{{ swagger_url }}", "/swagger.json"),
            content_type="text/html",
        )
