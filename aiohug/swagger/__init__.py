import importlib
import logging
from inspect import getfullargspec

from aiohttp import web
from apispec import APISpec
from apispec.ext.marshmallow.swagger import field2parameter
from defaultsettings import DefaultSettings
from marshmallow import fields, Schema
from marshmallow.schema import SchemaMeta

from arguments import get_default_args
from directives import get_available_directives
from .decorators import response, spec

logger = logging.getLogger(__name__)


class Settings(DefaultSettings):
    HOST = "localhost:9001"
    SCHEMES = ["http"]
    VERSION = "0.1"
    TITLE = "Swagger Application"
    DEFINITIONS_PATH = None
    TESTING_MODE = False
    USE_DEFAULT_RESPONSE = True
    DESCRIPTION = ""
    CONTACT_EMAIL = ""


settings = Settings("SWAGGER_")
del Settings


def get_summary(doc):
    if doc is not None:
        return doc.split("\n")[0]


def where_is_parameter(name, url):
    return "path" if "{%s}" % name in url else "query"


def get_parameters(url, handler, spec):
    defaults = get_default_args(handler._original_handler)
    args_spec = getfullargspec(handler._original_handler)
    parameters = []
    for name in args_spec.args:
        kind = args_spec.annotations.get(name, fields.Field())
        if name in get_available_directives() or name == "request":
            continue

        if isinstance(kind, fields.Field):
            parameter_place = where_is_parameter(name, url)
            kind.metadata = {"location": where_is_parameter(name, url)}
            kind.required = name not in defaults
            parameter = field2parameter(
                kind, name=name, default_in=parameter_place, use_refs=False
            )
            if name in defaults:
                parameter["default"] = defaults[name]
            parameters.append(parameter)
        # body
        elif name == "body" and (
            isinstance(kind, Schema) or isinstance(kind, SchemaMeta)
        ):
            if isinstance(kind, Schema):
                schema_name = kind.__class__.__name__
                schema = kind
            elif isinstance(kind, SchemaMeta):
                schema_name = kind.__name__
                schema = kind()

            spec.definition(schema_name, schema=schema)

            ref_definition = "#/definitions/{}".format(schema_name)
            ref_schema = {"$ref": ref_definition}

            parameters.append(
                {"in": "body", "name": "body", "required": True, "schema": ref_schema}
            )

    return parameters


def generate_swagger(app: web.Application):
    spec = APISpec(
        title=settings.TITLE,
        info={
            "description": settings.DESCRIPTION,
            "contact": {"email": settings.CONTACT_EMAIL},
        },
        version=settings.VERSION,
        plugins=("apispec.ext.marshmallow",),
        schemes=settings.SCHEMES,
        host=settings.HOST,
    )
    if settings.DEFINITIONS_PATH is not None:
        definitions = importlib.import_module(settings.DEFINITIONS_PATH)

        for name, schema in definitions.__dict__.items():  # type: str, Schema
            if name.endswith("Schema") and len(name) > len("Schema"):
                spec.definition(name, schema=schema)

    resources = app.router._resources
    for resource in resources:
        url = resource.canonical
        name = resource.name
        for route in resource._routes:
            method = route.method
            if method == "HEAD":
                continue

            handler = route._handler

            try:
                handler_spec = handler.swagger_spec
            except AttributeError:
                handler_spec = {}

            if "excluded" in handler_spec:
                continue

            try:
                handler_spec["summary"] = get_summary(handler.__doc__)
                handler_spec["description"] = handler.__doc__
            except KeyError:
                pass

            parameters = get_parameters(url, handler, spec)
            if parameters:
                handler_spec["parameters"] = parameters

            handler_spec["operationId"] = name

            spec.add_path(url, operations={method.lower(): handler_spec})

    return spec.to_dict()
