import aiohttp_jinja2
from aiohttp import web

from ...database.query import CompleteType, query_complete
from ...flow import Flow

routes = web.RouteTableDef()


MAX_COMPLETIONS = 100


@routes.get("/")
@aiohttp_jinja2.template("index.html.j2")
async def index(request):
    query = request.query.get("q", "")
    return {
        "query": query,
        "fields": Flow.field_names(),
    }


def field_completion(database, field, text):
    completions = []
    for flow in database.flows().find(limit=MAX_COMPLETIONS):
        value = getattr(flow, field)
        if value.startswith(text) and value not in completions:
            completions.append(value)
    return completions


@routes.post("/search/completion")
async def search_completion(request):
    """
    This provide the auto-completion for the search bar.
    """
    body = await request.json()
    query = body.get("q", "")

    completion_type, completions = query_complete(
        query,
        Flow.field_names(),
        lambda field, text: field_completion(request.app["database"], field, text),
    )

    result = []
    if completion_type == CompleteType.FIELD:
        kind = "field"
    else:
        kind = "value"
    for completion in completions:
        result.append(
            {
                "kind": kind,
                "text": completion,
                "label": completion,
            }
        )
    return web.json_response(result)
