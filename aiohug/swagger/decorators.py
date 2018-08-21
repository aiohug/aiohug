from typing import Optional, Iterable


def ensure_swagger_attr(handler):
    try:
        handler.swagger_spec
    except AttributeError:
        handler.swagger_spec = {"responses": {}}


def response(response_code, schema=None, description=None):
    """A decorator that adds swagger response"""

    def decorator(handler):
        ensure_swagger_attr(handler)
        handler.swagger_spec["responses"][response_code] = {}
        if schema is not None:
            handler.swagger_spec["responses"][response_code]["schema"] = schema
        if description is not None:
            handler.swagger_spec["responses"][response_code][
                "description"
            ] = description
        return handler

    return decorator


def spec(
    exclude: bool = False,
    private: bool = False,
    deprecated: bool = False,
    tags: Optional[Iterable] = None,
    response_codes: Optional[Iterable] = None,
):
    def decorator(handler):
        ensure_swagger_attr(handler)
        handler.swagger_spec["private"] = private
        handler.swagger_spec["exclude"] = exclude
        handler.swagger_spec["deprecated"] = deprecated
        if tags is not None:
            handler.swagger_spec["tags"] = tags
        if response_codes is not None:
            for code in response_codes:
                handler.swagger_spec["responses"][code] = {}

        return handler

    return decorator
