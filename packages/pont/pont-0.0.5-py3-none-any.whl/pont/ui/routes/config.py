import os

import aiohttp.web as web
import aiohttp_jinja2

routes = web.RouteTableDef()


@routes.get("/config", name="config")
@aiohttp_jinja2.template("config.html.j2")
async def config(request):
    settings = request.app["settings"]
    return {
        "config_file": settings.config_file,
        "current_directory": os.getcwd(),
        "settings": settings,
    }
