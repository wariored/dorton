A Python lightweight and fast framework for REST APIs

To get started: `pip install dorton`

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

You can use a class based handlers:

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
