"""
This boostrap the app with fake data
it's use to develop the UI
"""

import asyncio
import random

import aiohttp.web
import click

from pont.database.database import Database
from pont.flow import Flow
from pont.settings import Settings
from pont.ui import setup_app


def create_app(sleep: float = 0, iterations: int = 10) -> aiohttp.web.Application:
    app = setup_app()
    app["settings"] = Settings()
    app["settings"].load()
    app["database"] = Database()
    app["database"].flows().add(
        Flow(
            id="42424242",
            host="example.org",
            port=80,
            protocol="http",
            method="GET",
            status="200 OK",
            path="/hello",
            response_mime_type="text/html",
            request_headers={
                "User-Agent": "curl/7.64.1",
                "Accept": "*/*",
            },
            response_headers={
                "Content-Type": "text/html; charset=utf-8",
                "Content-Length": "42",
            },
            response_body=b"<html><body><b>Hello world</b></body></html>",
        )
    )
    app["database"].flows().add(
        Flow(
            id="42424243",
            host="example.org",
            port=80,
            protocol="http",
            status="200 OK",
            method="POST",
            path="/world",
            response_mime_type="application/json",
            request_headers={
                "User-Agent": "Firefox/7.64.1",
                "Accept": "application/jsons",
            },
            response_headers={
                "Content-Type": "application/json; charset=utf-8",
                "Content-Length": "42",
            },
            request_body=b'{"hello": "world"}',
            response_body=b'{"hello": "world", "foo": ["bar", "123"]}',
        )
    )
    app["database"].flows().add(
        Flow(
            protocol="redis",
            host="redis.local",
            port=6379,
            response_mime_type="application/redis",
            method="INCRBY",
            path="mykey",
            query="1",
        )
    )
    app["database"].flows().add(
        Flow(
            id="42424244",
            protocol="mysql",
            host="mysql.local",
            port=3306,
            response_mime_type="text/x-mysql",
            method="SELECT",
            path="posts",
            query="WHERE id=1",
            request_body=b"SELECT * FROM posts WHERE id=1",
        )
    )
    app["database"].flows().add(
        Flow(
            id="42424245",
            protocol="http",
            host="example.org",
            port=80,
            response_mime_type="application/javascript",
            method="GET",
            path="/app.js",
            response_body=b"// A comment\nfunction hello(a){\nconsole.log('Hello world');}",
        )
    )
    app["database"].flows().add(
        Flow(
            id="42424246",
            protocol="http",
            host="example.org",
            port=80,
            response_mime_type="text/css",
            method="GET",
            path="/style.css",
            response_body=open("pont/ui/static/style.css", "rb").read(),
        )
    )
    app["database"].flows().add(
        Flow(
            id="42424247",
            protocol="http",
            host="example.org",
            port=80,
            response_mime_type="text/xml",
            method="GET",
            path="/sitemap.xml",
            response_body=b"<sitemap><loc>https://example.org/</loc></sitemap>",
        )
    )
    app["sleep"] = sleep
    app["iterations"] = iterations
    app.cleanup_ctx.append(background_task)
    return app


async def flow_generator(app):
    i = 0
    try:
        while i < app["iterations"]:
            id = random.randint(0, 10000)
            app["database"].flows().add(
                Flow(
                    protocol="http",
                    host="example.org",
                    status="200 OK",
                    port=80,
                    method="GET",
                    path="/product",
                    query=f"id={id}",
                )
            )
            await asyncio.sleep(app["sleep"])
            i += 1
    except asyncio.CancelledError:
        pass


async def background_task(app):
    app["flow_generator"] = asyncio.create_task(flow_generator(app))
    yield
    app["flow_generator"].cancel()


@click.command()
@click.option(
    "--sleep",
    default=0,
    type=float,
    help="Sleep time between each flow generation in seconds",
)
@click.option(
    "--iterations",
    default=10,
    type=int,
    help="Number of iterations of the flow generation",
)
def demo(sleep: float, iterations: int):
    """
    Start the server with fake data. It's use to develop the UI.
    """
    aiohttp.web.run_app(create_app(sleep=sleep, iterations=iterations))
