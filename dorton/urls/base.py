import inspect

from dorton.http.enums import HttpRequestMethod

__all__ = ["Route"]


class Route:
    def __init__(self, path, handler, name=None, method=None):
        if not path.startswith("/"):
            path = "/" + path
        self.path = path

        if not inspect.isfunction(handler) and not inspect.isclass(handler):
            raise RuntimeError(
                "Route handler is expected to be a python function or class."
            )

        self.handler = handler

        # The route name is not being used yet
        self.name = name

        if method and method.upper() not in HttpRequestMethod.__members__:
            raise RuntimeError("Http method not recognized.")

        self.method = method.upper() if method else method

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.path}>"
