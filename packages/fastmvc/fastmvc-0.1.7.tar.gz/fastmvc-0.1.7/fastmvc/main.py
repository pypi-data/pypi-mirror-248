import typer
import os
from fastmvc import __version__
from fastmvc.generator import (
    build_base, gen_scaffold,
    gen_authlib, gen_simple_auth)
from typing import List
import fastmvc.utilities as utils

app = typer.Typer()


@app.command()
def version():
    """ show current version of FastMVC"""
    typer.echo(f"FastMVC {__version__}")


def __choose_platform(param_platform):
    plats = utils.platforms()
    if param_platform:
        try:
            selected_platform = utils.Platform[param_platform]
        except:
            selected_platform = None
    else:
        typer.secho('\n'.join(f"[{k}] {v.name}" for k, v in plats.items()))
        selected_platform = typer.prompt("Which platform would you like to build for?")
        selected_platform = plats.get(selected_platform)
    if not selected_platform:
        typer.secho(f"Please choose a valid Platform. {list(plats.values())}", fg='red')
    return selected_platform


@app.command()
def new(project: str, platform: str or None = None):
    """ create a new project """
    plat = __choose_platform(platform)
    if not plat:
        return

    new_folder = os.path.join(os.curdir, project)
    try:
        typer.secho(f"\nBuilding new project: {project}\n", fg='green')
        build_base(new_folder, project, plat)
        typer.echo(f"\n{project} was created.\n")
        if plat == utils.Platform.GOOGLE_APP_ENGINE and not utils.get_default_service_account_file():
            typer.secho("HINT: Don't forget to provide your service-account-file.json in the /ignore folder\n", fg="blue")
    except FileExistsError:
        typer.secho(f"'{project}' already exists in this folder.\n", fg='red')


@app.command()
def scaffold(obj: str, attributes: List[str], requires_login: bool = False):
    """ create a router and views for a described object """
    typer.secho(f"\nScaffolding views and router for: {obj}\n", fg='green')
    options = {'requires_login': requires_login}
    gen_scaffold(os.curdir, obj, attributes, options)
    typer.echo(f"\n{obj} was created.\n")


@app.command()
def auth():
    """ generate authorization framework for users """
    typer.secho(f"\nGenerating views and router for: User\n", fg='green')
    gen_authlib(os.curdir)
    typer.echo(f"\nAuth was created.\n")


@app.command()
def simple_auth():
    """ generate simple email authorization framework and users """
    typer.secho(f"\nGenerating views and router for: User\n", fg='green')
    gen_simple_auth(os.curdir)
    typer.echo(f"\nAuth was created.\n")
    if not utils.get_smtp_defaults():
        typer.secho("HINT: Don't forget to set your SMTP settings in the .env file\n", fg="blue")


@app.command()
def server():
    """ run the app locally """
    utils.run_server()


@app.command()
def s():
    """ alias for 'server' """
    server()


@app.command()
def view_config():
    """ view your development configurations """
    conf = utils.config()
    typer.echo(conf)


@app.command()
def set_smtp_defaults():
    """ Set SMTP Defaults based on current project's SMTP Settings in ENV """
    utils.set_default_smtp_from_current_project()
    typer.secho('SMTP Defaults set.', fg='green')


@app.command()
def set_service_account_defaults():
    """ Set default service account file based on current project's service account file """
    utils.set_default_service_account_file_from_current_project()


@app.command()
def help(subject: str):
    """ try: 'fastmvc help gcloud' """
    if subject == 'gcloud':
        typer.echo("""
        GCLOUD COMMANDS:\n
        gcloud init              -- choose your configuration file for gcloud
        gcloud app create        -- create a new app in configured gcloud
        gcloud app deploy        -- upload files and create a new version of app in cloud.
        """)
