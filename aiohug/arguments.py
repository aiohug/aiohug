from inspect import iscoroutine, signature, Parameter, isclass, getfullargspec
from typing import Optional
from marshmallow import ValidationError, fields, Schema
from aiohttp import web

from .directives import get_directive


def get_default_args(func):
    sig = signature(func)
    return {
        k: v.default
        for k, v in sig.parameters.items()
        if v.default is not Parameter.empty
    }


def get_arg(request, arg_name, defaults):
    if arg_name == "request":
        return request

    # get args from directives
    try:
        return get_directive(arg_name)(request)
    except KeyError:
        pass

    # get args from path
    try:
        return request.match_info[arg_name]
    except KeyError:
        pass

    # get args from query
    try:
        return request.rel_url.query[arg_name]
    except KeyError:
        pass

    try:
        return defaults[arg_name]
    except KeyError:
        raise fields.ValidationError("Required argument")


def cast_arg(arg, kind: Optional = None):
    # fields.Integer()
    if isinstance(kind, fields.Field):
        arg = kind.deserialize(arg)
    # arg: fields.Integer
    elif isclass(kind) and issubclass(kind, fields.Field):
        arg = kind().deserialize(arg)
    # arg: RequestSchema
    elif isclass(kind) and issubclass(kind, Schema):
        arg = kind(strict=True, many=False).dump(arg).data
    # RequestSchema()
    elif isinstance(kind, Schema):
        kind.strict = True
        arg = kind.dump(arg).data
    # int, string
    elif callable(kind):
        arg = kind(arg)

    return arg


async def get_kwargs(request: web.Request, handler):
    defaults = get_default_args(handler)
    arg_spec = getfullargspec(handler)
    kwargs = {}
    errors = {}
    for arg_name in arg_spec.args:
        try:
            arg = get_arg(request, arg_name, defaults)
            arg = await arg if iscoroutine(arg) else arg
            arg = cast_arg(arg, arg_spec.annotations.get(arg_name))
        except ValidationError as e:
            errors[arg_name] = e.messages
        else:
            if arg is not None:
                kwargs[arg_name] = arg
    return kwargs, errors
