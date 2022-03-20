# Flask Web Calendar API

Structure of `api` catalog:

```text
api
├── __init__.py
├── common
│   ├── models
│   │   ├── __init__.py
│   │   └── event.py
│   └── schemas
│       ├── __init__.py
│       └── event.py
├── v1
│   ├── __init__.py
│   ├── api.py
│   └── event.py
└── v2
    ├── __init__.py
    ├── api.py
    └── event.py
```

## version 1

API ver.1 use view as functions.

Benefits:

- this is simple (easy write, easy read, easy understand)

- this is flexible (if you need a new route like `/event/today` just add a new function)

- you can use autodocumentation in OpenAPI format (swagger) (use: `apispec` package)

Drawbacks:

- 'bad' way to connect resource

    ```python
    # ./api/v1/api.py
    # for load resource you need import this
    from .event import api
    ```

- with a large number of routes, it can be difficult to read

## version 2

API ver.1 use view as MethodView class.

Benefits:

- this is laconically

- all of one resource logic in one class

- 'pretty' way to connect resource (IMHO)

    ```python
    # ./api/v2/api.py
    from .event import EventResource
    ...
    EventResource.register(api)
    ```

Drawbacks:

- makes methods (get, post and etc.) more larger

- unable to auto-document to OpenAPI

## Conclusion

The Flask MethodView class is suitable for implementing simple REST resources with manual documentation.

The standard view-as-function approach remains the preferred one (for me).
