import pathlib


def generate_base_app_files(app_path):
    """
    Creates common base files for apps
    """
    handlers = pathlib.Path(f"{app_path}/handlers.py")
    handlers.touch()
    handlers.write_text(DEFAULT_HANDLER_CODE)

    routes = pathlib.Path(f"{app_path}/routes.py")
    routes.touch()
    app_name = app_path.split("/")[-1]
    routes.write_text(DEFAULT_ROUTES_CODE % (app_name, app_name))

    models = pathlib.Path(f"{app_path}/models.py")
    models.touch()
    models.write_text("# Write here the app models")


DEFAULT_HANDLER_CODE = """
# Write here the handlers of your routes

def index(request):
    return {"ok": True}

"""

DEFAULT_ROUTES_CODE = """
# Write here the urls patterns

from dorton.urls import Route
from . import handlers

patterns = [
    Route("%s/", handlers.index, name="%s")
]

"""
