import aiohttp_jinja2
from aiohttp import web

from pont.flow import Flow
from pont.renderer import render

routes = web.RouteTableDef()


def get_flow(request) -> Flow:
    try:
        return request.app["database"].flows().get(request.match_info["id"])
    except KeyError:
        raise web.HTTPNotFound()


@routes.get("/flows/{id}", name="flow")
@aiohttp_jinja2.template("flow/summary.html.j2")
async def flow(request):
    return {"flow": get_flow(request), "route": "flow"}


@routes.get("/flows/{id}/request/headers", name="flow_request_headers")
@aiohttp_jinja2.template("flow/headers.html.j2")
async def flow_request_headers(request):
    flow = get_flow(request)
    return {
        "flow": flow,
        "route": "flow_request_headers",
        "headers": flow.request_headers,
    }


@routes.get("/flows/{id}/response/headers", name="flow_response_headers")
@aiohttp_jinja2.template("flow/headers.html.j2")
async def flow_response_headers(request):
    flow = get_flow(request)
    return {
        "flow": flow,
        "route": "flow_response_headers",
        "headers": flow.response_headers,
    }


@routes.get("/flows/{id}/request/body", name="flow_request_body")
@aiohttp_jinja2.template("flow/body.html.j2")
async def flow_request_body(request):
    flow = get_flow(request)
    template_renderer, context = render(flow, flow.request_body)
    context.update(
        {
            "flow": flow,
            "route": "flow_response_body",
            "template_renderer": template_renderer,
        }
    )
    return context


@routes.get("/flows/{id}/response/body", name="flow_response_body")
@aiohttp_jinja2.template("flow/body.html.j2")
async def flow_response_body(request):
    flow = get_flow(request)
    template_renderer, context = render(flow, flow.response_body)
    context.update(
        {
            "flow": flow,
            "route": "flow_response_body",
            "template_renderer": template_renderer,
        }
    )
    return context
