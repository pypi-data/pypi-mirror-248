import pytest

from pont.protocols.http import HTTP
from pont.protocols.protocol import Protocol
from pont.tests.protocols.helpers import (
    assert_client_write,
    assert_remote_connect,
    assert_remote_ssl_connect,
    assert_remote_write,
    mock_request,
    mock_response,
)


@pytest.fixture
def http(create_protocol) -> Protocol:
    return create_protocol(HTTP)


def test_parse_header_line(http):
    header_line = b"Content-Type: application/json\r\n"
    header_name, header_value = http._parse_header_line(header_line)
    assert header_name == "Content-Type"
    assert header_value == "application/json"


def test_parse_http11_get(http):
    flow = mock_request(
        http, b"""GET http://example.org/ HTTP/1.1\r\nHost: example.org\r\n\r\n"""
    )
    mock_response(
        http,
        b"""HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\nHello world""",
    )
    assert_remote_write(http, b"GET / HTTP/1.1\r\nHost: example.org\r\n\r\n")
    assert_remote_connect(http, "example.org", 80)
    assert_client_write(
        http, b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\nHello world"
    )
    assert flow.host == "example.org"
    assert flow.port == 80
    assert flow.method == "GET"
    assert flow.path == "/"
    assert flow.query == ""
    assert flow.request_headers == {"Host": "example.org"}
    assert flow.request_body == b""
    assert flow.protocol == "http"
    assert flow.status == "200 OK"
    assert flow.response_mime_type == "text/html"
    assert flow.response_headers == {"Content-Type": "text/html"}
    assert flow.response_body == b"Hello world"


def test_parse_http11_post(http):
    flow = mock_request(
        http,
        b"""POST http://example.org/contents/new?a=1 HTTP/1.1\r\nHost: example.org\r\nContent-Type: application/json\r\n\r\n{"a": 1}""",
    )
    mock_response(
        http,
        b"""HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\nHello world""",
    )
    assert flow.method == "POST"
    assert flow.path == "/contents/new"
    assert flow.query == "a=1"
    assert flow.request_headers == {
        "Host": "example.org",
        "Content-Type": "application/json",
    }
    assert flow.request_body == b"""{"a": 1}"""
    assert flow.protocol == "http"
    assert flow.status == "200 OK"
    assert flow.response_mime_type == "text/html"
    assert flow.response_headers == {"Content-Type": "text/html"}
    assert flow.response_body == b"Hello world"
    assert_remote_connect(http, "example.org", 80)
    assert_remote_write(
        http,
        b"""POST /contents/new?a=1 HTTP/1.1\r\nHost: example.org\r\n"""
        b"""Content-Type: application/json\r\n\r\n{"a": 1}""",
    )
    assert_client_write(
        http,
        b"""HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\nHello world""",
    )


def test_charset_in_mimetype(http):
    flow = mock_request(
        http,
        b"""POST http://example.org/contents/new?a=1 HTTP/1.1\r\nHost: example.org\r\nContent-Type: application/json\r\n\r\n{"a": 1}""",
    )
    mock_response(
        http,
        b"""HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\nHello world""",
    )
    assert flow.response_mime_type == "text/html"


def test_https(http, database):
    mock_request(
        http,
        b"""CONNECT example.org:443 HTTP/1.1\r\nHost: example.org\r\n\r\nGET http://example.org/ HTTP/1.1\r\nHost: example.org\r\n\r\n""",
    )
    mock_response(
        http,
        b"""HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\nHello world""",
    )
    assert len(database.flows().find()) == 2
    connect_flow = database.flows().find()[0]
    assert connect_flow.protocol == "https"
    assert connect_flow.method == "CONNECT"
    assert connect_flow.host == "example.org"
    assert connect_flow.port == 443

    get_flow = database.flows().find()[1]
    assert get_flow.protocol == "http"
    assert get_flow.method == "GET"
    assert get_flow.host == "example.org"
    assert get_flow.port == 80
    assert get_flow.path == "/"

    assert_client_write(
        http,
        b"HTTP/1.1 200 OK\r\n\r\nHTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\nHello world",
    )

    assert_remote_ssl_connect(http, "example.org", 443)

    assert_client_write(
        http,
        b"HTTP/1.1 200 OK\r\n\r\nHTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\nHello world",
    )

    assert_remote_ssl_connect(http, "example.org", 443)
