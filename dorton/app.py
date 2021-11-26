import json

import jsonpickle
from webob import Request, Response

from dorton.core.handlers.base import HttpHandler
from dorton.exceptions import RouteMethodNotFoundError, RouteNotFoundError
from dorton.http import APIResponse

DEFAULT_CONTENT_TYPE = "application/json"


class App(HttpHandler):
    def __call__(self, environ, start_response):
        request = Request(environ)
        response = self.handle_request(request)
        response.content_type = DEFAULT_CONTENT_TYPE
        return response(environ, start_response)

    def _default_response(self, response):
        response.status_code = 404
        response.json = "Not found."

    def handle_request(self, request: Request):
        """
        Fetch the corresponding route and execute the request

        :return WSGI response
        """
        response = Response()
        path = request.path

        try:
            handler, method, kwargs = self._find_handler(path)
        except RouteNotFoundError:
            self._default_response(response)
            return response

        if method and method != request.method:
            self._default_response(response)
        else:
            try:
                res = self._get_handler_response(request, handler, kwargs)
            except RouteMethodNotFoundError:
                self._default_response(response)
                return response
            
            if isinstance(res, APIResponse):
                response.json = res.toJSON()
                response.content_type = res.content_type
                response.status_code = res.status_code
            else:
                response.json = json.loads(
                    jsonpickle.encode(res, unpicklable=False, indent=2)
                )

        return response
