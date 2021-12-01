import importlib


class AppConfig:
    def __init__(self, app_name):
        self.app_name = app_name

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.app_name}>"

    @property
    def routes(self):
        return self._get_routes()

    def _get_routes(self):
        routes = importlib.import_module(f"{self.app_name}.routes")
        return routes.patterns
