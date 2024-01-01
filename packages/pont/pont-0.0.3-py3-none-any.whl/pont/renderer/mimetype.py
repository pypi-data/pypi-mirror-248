from typing import Tuple

from ..flow import Flow


def render(flow: Flow, content: bytes) -> Tuple[str, dict]:
    """
    Render the response content of a flow message based on the mime type.

    Args:
        flow: The flow message.
        content: The response content.
    Returns:
        The rendered response content as HTML safe string.
    """
    language = flow.response_mime_type.split("/")[1]
    if language == "xml":
        language = "html"
    return ("mimetype", {"language": language, "content": content.decode("utf-8")})
