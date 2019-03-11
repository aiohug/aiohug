# 0.6.2

* Support decorators for handlers

```python
from functools import wraps
from aiohug import RouteTableDef

routes = RouteTableDef()

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

```

# 0.6.1

* Support prefix for handlers

```python
from aiohug import RouteTableDef

monitoring_routes = RouteTableDef(prefix="monitoring")

@monitoring_routes.get("/ping/")
async def hello():
    return "pong"
    
```

# 0.5

* Support marshmallow 3 instead of 2
