from aiohttp import web

try:
    from aiohttp.web_routedef import RouteDef
except ImportError:  # pragma: no cover
    from aiohttp.web_urldispatcher import RouteDef

from .arguments import get_kwargs
from . import shortcuts


def _handle(handler):
    async def _handler(request):
        kwargs, errors = await get_kwargs(request, handler)

        if errors:
            return web.json_response(
                {"status": "error", "data": errors}, status=web.HTTPConflict.status_code
            )

        resp = await handler(**kwargs)
        resp = shortcuts.process_response(resp)
        return resp

    _handler._original_handler = handler
    return _handler


class RouteTableDef(web.RouteTableDef):
    def __init__(self, prefix="") -> None:
        super().__init__()
        prefix = prefix.strip("/")
        self.path_prefix = "/" + prefix if prefix != "" else prefix

    def route(self, method, path, **kwargs):
        def inner(handler):
            handler = _handle(handler)
            self._items.append(
                RouteDef(method, f"{self.path_prefix}{path}", handler, kwargs)
            )
            return handler

        return inner
