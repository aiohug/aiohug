# 0.6.1

* Support prefix for handlers

```python
monitoring_routes = RouteTableDef(prefix="monitoring")

@monitoring_routes.get("/ping/")
async def hello():
    return "pong"
    
```

# 0.5

* Support marshmallow 3 instead of 2
