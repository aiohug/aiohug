_available_directives = {}


def directive(fn):
    _available_directives[fn.__name__] = fn
    fn._directive = True
    return fn


def get_directive(fn):
    return _available_directives[fn]


def get_available_directives():
    return _available_directives


@directive
async def body(request):
    return await request.json()
