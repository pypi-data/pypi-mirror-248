import asyncio
import logging
import os
import signal
from pathlib import Path
from typing import AsyncIterator

import aiohttp.web
import click

from ..database.database import Database
from ..protocols.http import HTTP
from ..proxy import Proxy
from ..settings import Settings, SettingsError
from ..ui import setup_app


async def listen(app: aiohttp.web.Application) -> AsyncIterator[None]:
    tasks = [asyncio.create_task(proxy.start()) for proxy in app["proxies"]]
    if len(tasks):
        await asyncio.wait(tasks)
    yield


def pidfile_path() -> Path:
    settings = Settings()
    if settings.project_config_directory().exists():
        return settings.project_config_directory() / "pont.pid"
    return settings.user_config_directory() / "pont.pid"


def create_app() -> aiohttp.web.Application:
    # Log on console
    logging.basicConfig(level=logging.INFO)
    app = setup_app()
    app["settings"] = Settings()
    try:
        app["settings"].load()
    except SettingsError as error:
        logging.error(error)
        exit(1)
    app["database"] = Database()
    app["proxies"] = []
    for proxy in app["settings"].proxies:
        if proxy.protocol == "http":
            app["proxies"].append(Proxy(app["database"], proxy, HTTP))
    app.cleanup_ctx.append(listen)
    return app


@click.command()
def run():
    """
    Start the server and do not detach from the console.
    """
    app = create_app()
    settings = app["settings"]
    logging.info(f"UI listening on http://{settings.host}:{settings.port}")
    aiohttp.web.run_app(
        app, host=settings.host, port=settings.port, print=None, access_log=None
    )


@click.command()
@click.option(
    "--pidfile", default=lambda: pidfile_path(), type=click.Path(path_type=Path)
)
@click.pass_context
def start(ctx: click.Context, pidfile: Path, **kwargs):
    """
    Start the server in background.
    """

    if pidfile.exists():
        logging.error(f"Pid file already exists: {pidfile}")
        exit(1)
    newpid = os.fork()
    if newpid == 0:
        # Child process
        pidfile.parent.mkdir(parents=True, exist_ok=True)
        with pidfile.open("w+") as f:
            f.write(str(os.getpid()))
        ctx.invoke(run, **kwargs)
    else:
        exit(0)


@click.command()
@click.option(
    "--pidfile",
    default=lambda: pidfile_path(),
    type=click.Path(path_type=Path),
)
def stop(pidfile: Path):
    """
    Stop the server.
    """
    if pidfile.exists():
        try:
            with pidfile.open() as f:
                pid = int(f.read())
                try:
                    os.kill(pid, signal.SIGTERM)
                    pidfile.unlink()
                except ProcessLookupError:
                    logging.error(
                        f"Process {pid} not found. Removing pid file {pidfile}."
                    )
                    pidfile.unlink()
        except OSError as error:
            logging.error(error)

    else:
        logging.error(f"No pid file found: {pidfile}")


@click.command()
@click.option(
    "--pidfile", default=lambda: pidfile_path(), type=click.Path(path_type=Path)
)
@click.pass_context
def shell(ctx: click.Context, pidfile: Path, **kwargs):
    """
    Start a shell with the proxy settings exported to the environment variables.
    """

    if pidfile.exists():
        logging.info("Server already running")
        newpid = -1
    else:
        newpid = os.fork()
    if newpid == 0:
        # Child process
        pidfile.parent.mkdir(parents=True, exist_ok=True)
        with pidfile.open("w+") as f:
            f.write(str(os.getpid()))
        ctx.invoke(run, **kwargs)
    else:
        app = create_app()
        settings = app["settings"]
        for proxy in settings.proxies:
            # TODO: Make it more generic
            if proxy.protocol == "http":
                os.environ[
                    "http_proxy"
                ] = f"http://{proxy.local_host}:{proxy.local_port}"
                os.environ[
                    "https_proxy"
                ] = f"http://{proxy.local_host}:{proxy.local_port}"
        logging.info("Proxy settings exported to the environment variables")
        os.execv(os.environ["SHELL"], [os.environ["SHELL"]])
