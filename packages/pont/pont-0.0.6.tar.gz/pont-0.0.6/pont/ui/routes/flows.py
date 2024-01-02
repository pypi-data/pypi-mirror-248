import urllib.parse

import aiohttp.web as web
import aiohttp_jinja2

from pont.database import QueryError

routes = web.RouteTableDef()

MAX_RESULTS = 100


def _update_browser_url(request, response, query):
    """
    Update the browser URL to reflect the current query

    This is done by setting the `HX-Replace-Url` header on the response
    HTMX will then update the browser URL to the value of this header.
    """
    current_url = request.headers.get("HX-Current-URL")
    if current_url and query is None:
        response.headers["HX-Replace-Url"] = current_url
    if current_url and query is not None:
        parsed_url = urllib.parse.urlparse(current_url)
        response.headers["HX-Replace-Url"] = urllib.parse.urlunparse(
            (
                parsed_url.scheme,
                parsed_url.netloc,
                parsed_url.path,
                parsed_url.params,
                urllib.parse.urlencode({"q": query}),
                parsed_url.fragment,
            )
        )


@routes.get("/components/flows")
async def flows(request):
    query = request.query.get("q")
    try:
        flows = (
            request.app["database"]
            .flows()
            .find(query=query, limit=MAX_RESULTS, reverse=True)
        )
        if request.headers.get("If-Modified-Since"):
            last_modified = request.headers.get("If-Modified-Since")
            if len(flows) > 0 and last_modified == flows[0].updated_at.isoformat():
                return web.Response(status=304)

        context = {
            "flows": flows,
        }
        response = aiohttp_jinja2.render_template(
            "components/flows.html.j2", request, context
        )
        if len(flows) > 0:
            response.headers["Last-Modified"] = flows[0].updated_at.isoformat()
        _update_browser_url(request, response, query)
        return response
    except QueryError as e:
        response = aiohttp_jinja2.render_template(
            "components/error.html.j2", request, {"message": str(e)}
        )
        _update_browser_url(request, response, query)
        return response


@routes.delete("/components/flows")
async def delete_flows(request):
    request.app["database"].flows().clear()
    context = {
        "flows": [],
    }
    response = aiohttp_jinja2.render_template(
        "components/flows.html.j2", request, context
    )
    return response
