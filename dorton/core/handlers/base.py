import importlib
import inspect
from types import FunctionType

from dorton.exceptions import (
    RouteMethodNotFoundError,
    RouteNotFoundError,
    RouteValueError,
)
from dorton.urls.base import Route
from parse import parse


class HttpHandler:
    def __init__(self) -> None:
        self.routes = {}

    def _add_route(self, handler: FunctionType, path: str, method: str = None):
        if path in self.routes:
            raise RouteValueError(f"Route {path} already exists.")
        self.routes[path] = (handler, method)

    def _get_handler_response(self, request, handler, kwargs):
        if inspect.isclass(handler):
            handler = getattr(handler(), request.method.lower(), None)
            if handler is None:
                raise RouteMethodNotFoundError
        if kwargs:
            return handler(request, **kwargs)
        return handler(request)

    def _find_handler(self, request_path):
        for path, value in self.routes.items():
            handler, method = value
            parse_result = parse(path, request_path)
            if parse_result is not None:
                return handler, method, parse_result.named
            elif request_path == path:
                return handler, method, None

        raise RouteNotFoundError

    def route(self, path):
        """
        Decorator that handles the framework routes

        Args:
            path (str): route path value
        """

        def wrapper(handler):
            self._add_route(handler, path)
            return handler

        return wrapper

    def get(self, path):
        def wrapper(handler):
            self._add_route(handler, path, "GET")
            return handler

        return wrapper

    def post(self, path):
        def wrapper(handler):
            self._add_route(handler, path, "POST")
            return handler

        return wrapper

    def put(self, path):
        def wrapper(handler):
            self._add_route(handler, path, "PUT")
            return handler

        return wrapper

    def delete(self, path):
        def wrapper(handler):
            self._add_route(handler, path, "DELETE")
            return handler

        return wrapper

    def patch(self, path):
        def wrapper(handler):
            self._add_route(handler, path, "PATCH")
            return handler

        return wrapper

    def register_routes(self):
        try:
            settings = importlib.import_module("settings")
        except ModuleNotFoundError:
            pass
        else:
            # register routes in each app in settings
            for app_name in settings.LIST_APPS:
                routes = importlib.import_module(f"{app_name}.routes")
                for route in routes.patterns:
                    if not isinstance(route, Route):
                        raise RouteValueError(
                            "Each value of the variable patterns should be instance of Route"
                        )
                    self._add_route(route.handler, route.path, route.method)

    def register(self):
        self.register_routes()
