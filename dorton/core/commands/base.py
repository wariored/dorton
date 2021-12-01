import importlib
import os
import pathlib

import click
from dorton.core.commands.utils import generate_base_app_files

__all__ = ["execute_commands"]


def execute_commands():
    cli()


@click.group()
def cli():
    pass


@click.command(help="create the base project")
@click.argument("name")
def initproject(name):
    """Program that creates the project directory and files"""

    # path at terminal when executing the command
    base_path = os.getcwd() + "/" + name
    base = pathlib.Path(base_path)
    if base.exists():
        click.secho(f"Directory '{name}' already exists.", fg="red")
        return
    base.mkdir(parents=True)

    first_app_path = base_path + "/" + name
    pathlib.Path(first_app_path).mkdir(parents=True)

    generate_base_app_files(first_app_path)

    starter = pathlib.Path(f"{base_path}/app.py")
    starter.touch()
    starter.write_text(STARTER_DEFAULT_CODE)

    settings = pathlib.Path(f"{base_path}/settings.py")
    settings.touch()
    settings.write_text(DEFAULT_SETTINGS % name)

    click.secho("Done!", fg="green")


@click.command(help="create an app in the project")
@click.argument("name")
def initapp(name):
    base_path = os.getcwd()
    app_path = f"{base_path}/{name}"
    app = pathlib.Path(app_path)
    if app.exists():
        click.secho(f"App with name '{name}' already exists.", fg="red")
        return
    app.mkdir(parents=True)

    generate_base_app_files(app_path)

    click.secho("Done!", fg="green")


cli.add_command(initproject)
cli.add_command(initapp)


DEFAULT_SETTINGS = """
DEBUG = True

# Add here the apps in order for dorton to loads them
LIST_APPS = [
    '%s',
]

# Databases settings
DATABASES = {
    'default':{
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'TARGET': 'postgres'
    }
}
"""

STARTER_DEFAULT_CODE = """
# Where everything starts

from dorton.app import App

app = App()
app.register()

"""
