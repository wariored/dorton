from dorton.app import App
from dorton.http.response import APIResponse
from dorton.http.enums import HttpStatusCode

app = App()


class CustomResponse:
    def __init__(self) -> None:
        self.name = "cheikh"
        self.last_name = "konteye"


@app.route("/home")
def home(request):
    return {"ok": True}


@app.get("/get/{name}")
def get_name(request, name):
    return {"get": "ok", "name": name}


@app.post("/post")
def post_name(request):
    return CustomResponse()


@app.get("/custom-response")
def custom_response(request):
    content = {"test": 1, "zed": True}
    return APIResponse(content=content, status_code=HttpStatusCode.ACCEPTED)


@app.route("/class-based")
class ClassBasedController:
    def get(self, request):
        return APIResponse(content={"ok": "get worked"})

    def post(self, request):
        return APIResponse(content={"ok": "post worked"})
