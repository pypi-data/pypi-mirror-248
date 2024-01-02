from pont.flow import Flow
from pont.renderer import render


def test_render_html():
    flow = Flow("http", id="1", path="/hello")
    flow.response_mime_type = "text/html"
    flow.response_body = b"<html><body><h1>Hello</h1></body></html>"
    assert (
        "mimetype",
        {"language": "html", "content": flow.response_body.decode("utf-8")},
    ) == render(flow, flow.response_body)


def test_render_json():
    flow = Flow("http", id="1", path="/hello")
    flow.response_mime_type = "application/json"
    flow.response_body = b'{"hello": "world"}'
    assert (
        "mimetype",
        {"language": "json", "content": flow.response_body.decode("utf-8")},
    ) == render(flow, flow.response_body)


def test_render_css():
    flow = Flow("http", id="1", path="/hello")
    flow.response_mime_type = "text/css"
    flow.response_body = b"body { background: red; }"
    assert (
        "mimetype",
        {"language": "css", "content": flow.response_body.decode("utf-8")},
    ) == render(flow, flow.response_body)


def test_render_xml():
    flow = Flow("http", id="1", path="/hello")
    flow.response_mime_type = "text/xml"
    flow.response_body = b"<sitemap><loc>https://example.org/</loc></sitemap>"
    assert (
        "mimetype",
        {"language": "html", "content": flow.response_body.decode("utf-8")},
    ) == render(flow, flow.response_body)


def test_render_unknown():
    flow = Flow("http", id="1", path="/hello")
    flow.response_mime_type = "application/unknown"
    flow.response_body = b"<script>console.log('hello');</script>"
    assert (
        "unknown",
        {"content": flow.response_body.decode("utf-8")},
    ) == render(flow, flow.response_body)
