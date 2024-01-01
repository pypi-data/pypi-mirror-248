from typing import Tuple

from ..flow import Flow
from . import mimetype

RENDERERS = {
    "application/json": mimetype.render,
    "application/javascript": mimetype.render,
    "text/html": mimetype.render,
    "text/css": mimetype.render,
    "text/xml": mimetype.render,
    "application/xml": mimetype.render,
}


def render_unknown(_flow: Flow, content: bytes) -> Tuple[str, dict]:
    return ("unknown", {"content": content.decode("utf-8")})


def render(flow: Flow, content: bytes) -> Tuple[str, dict]:
    """
    Render the response content of a flow message based on the mime type.
    Multiple renderers can be registered. If the mime type is not registered
    a default renderer will be used.

    Args:
        flow: The flow message.
        content: The response content.
    Returns:
        Tuple of the jinja2 template name and the context.
    """
    if flow.response_mime_type in RENDERERS:
        return RENDERERS[flow.response_mime_type](flow, content)
    return render_unknown(flow, content)
