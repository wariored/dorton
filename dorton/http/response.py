import json

import jsonpickle
from dorton.http.enums import HttpStatusCode

__all__ = [
    "APIResponse"
]

class APIResponse:
    def __init__(
        self,
        content,
        content_type="application/json",
        status_code=HttpStatusCode.OK,
    ) -> None:
        self.content = content
        self.content_type = content_type
        self.status_code = status_code

    def toJSON(self):
        return json.loads(jsonpickle.encode(self.content, unpicklable=False, indent=2))
