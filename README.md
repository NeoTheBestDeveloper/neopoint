# Neopoint

## Warning - project is unstable.

Neopoint is a simple backend framework, which support routing, parsing query and path parametrs etc.

## Examples

### Create base app

```python
from neopoint import App
from neopoint.routing import Router


router = Router(prefix="/api")

app = App(debug=True)
app.include_router(router)
```

### Let's add some endpoints
```py 
from neopoint.http import JsonResponse

@router.get("/users/{user_id}")
def get_user_by_id(user_id: int) -> JsonResponse:
    return JsonResponse(
        {
            "id": user_id,
            "first_name": "John",
            "last_name": "Doe",
        }
    )
```


You can add pattern at endpoint path like {NAME_OF_PARAMETR} and it will be passed to your controller function.

### Let's parse also query parametrs.

```py 
from neopoint.http import JsonResponse

@router.get("/users")
def get_users(limit: int = 15, sort: str = "ASC") -> JsonResponse:
    return JsonResponse(
        {
            "id": user_id,
            "limit": limit,
            "sort": sort,
        }
    )
```

### How to handle post and other requests with payload?

```python
@router.post("/theme")
def create_theme(req: Request) -> JsonResponse:
    return JsonResponse(req.json)
```

For handling requests you can pass request parametr to your controller.

Request attributes:
- headers -> MappingProxyType\[str, str]
- query_params -> QueryParams
- path_params -> PathParams
- method -> RequestMethod
- path -> str
- json -> Any
- content -> bytes
