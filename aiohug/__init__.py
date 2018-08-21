from aiohttp import web
from aiohttp.web_routedef import RouteDef

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
    def route(self, method, path, **kwargs):
        def inner(handler):
            handler = _handle(handler)
            self._items.append(RouteDef(method, path, handler, kwargs))
            return handler

        return inner
