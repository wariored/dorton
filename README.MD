A Python lightweight and fast framework for REST APIs

To get started: `pip install dorton`

## Basic Usage

With function based handlers
```python
from dorton.app import App

app = App()

@app.route("/home")
def home(request):
    return {"ok": True}

```
Use `gunicorn` to get the server started with the command: `gunicorn init:app --bind=127.0.0.1:8000 --reload`

You can also return a custom response or pass a parameter to the url

```python
app = App()

class CustomResponse:
    def __init__(self, name) -> None:
        self.name = name

@app.get("/get/{name}")
def get_name(request, name):
    return CustomResponse(name)
```

You can use a class based handler:

```python
from dorton.app import App
from dorton.http.response import APIResponse
from dorton.http.enums import HttpStatusCode

app = App()

@app.route("/class-based")
class ClassBasedController:
    def get(self, request):
        return APIResponse(content={"ok": "get worked"}, status_code=HttpStatusCode.ACCEPTED)

    def post(self, request):
        return APIResponse(content={"ok": "post worked"}, status_code=HttpStatusCode.OK)
````

## Usage like Django projects

Create the project with: `python -m dorton initproject my_project`

Default files are created with boilerplates to get started:
```
my_project/
    my_projects/
        handlers.py
        models.py
        routes.py
    app.py
    settings.py
```
Run the server with: 

`gunicorn app:app --bind=127.0.0.1:8000 --reload`

You can add more apps: 

`cd my_project`

`python -m dorton initapp products` 

A new app with default structure will be created:
```
my_project/
    products/
        handlers.py
        models.py
        routes.py
    my_projects
    app.py
    settings.py
```
Add the new app name to the settings "LIST_APPS" and it will be recognized by dorton.

You can now add a handler in your handlers file:
```python
# products/handlers.py

def my_handler(request):
    res = ["orange", "apple"]
    return {"result": res}
```

Add the corresponding route:
```python
# products/routes.py

from dorton.urls import Route
from .handlers import my_handler

patterns = [
    Route("products/fruits-list", my_handler, method="get", name="fruits-list")
]
```

The handler `my_handler` will be hitted whenever your make a GET request through the url `products/fruits-list`.
