import importlib
import logging
from inspect import getfullargspec

from aiohttp import web
from apispec import APISpec
from apispec.ext.marshmallow import OpenAPIConverter

from marshmallow import fields, Schema
from marshmallow.schema import SchemaMeta

from aiohug.arguments import get_default_args
from aiohug.directives import get_available_directives
from .decorators import response, spec

logger = logging.getLogger(__name__)

converter = OpenAPIConverter("2.1")

DEFAULT_HOST = "localhost:8080"
DEFAULT_SCHEMES = ["http"]
DEFAULT_VERSION = None
DEFAULT_TITLE = "Swagger Application"
DEFAULT_DEFINITIONS_PATH = None
DEFAULT_TESTING_MODE = False
DEFAULT_USE_DEFAULT_RESPONSE = True
DEFAULT_DESCRIPTION = None
DEFAULT_CONTACT_EMAIL = None

PARAMETER_IN_PATH = "path"
PARAMETER_IN_QUERY = "query"


def get_summary(doc):
    if doc is not None:
        return doc.split("\n")[0]


def where_is_parameter(name, url):
    return PARAMETER_IN_PATH if "{%s}" % name in url else PARAMETER_IN_QUERY


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
            parameter = converter.field2parameter(
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


def generate_swagger(
    app: web.Application,
    title=DEFAULT_TITLE,
    version=DEFAULT_VERSION,
    host=DEFAULT_HOST,
    schemes=DEFAULT_SCHEMES,
    definitions_path=DEFAULT_DEFINITIONS_PATH,
    **options
):
    if host is not None:
        options["host"] = host
    if schemes is not None:
        options["schemes"] = schemes

    spec = APISpec(
        title=title, version=version, plugins=("apispec.ext.marshmallow",), **options
    )
    if definitions_path is not None:
        definitions = importlib.import_module(definitions_path)

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
