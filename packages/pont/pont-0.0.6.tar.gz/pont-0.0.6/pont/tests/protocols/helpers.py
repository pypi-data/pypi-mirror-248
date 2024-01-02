"""
Protocol helper functions for testing

Examples:
    >>> from .helpers import create_protocol
    >>> from pont.protocols.http import HTTP
    >>>
    >>> def test_parse_http11_get(create_protocol):
    >>>     http = create_protocol(HTTP)
    >>>     mock_request(http, b"GET / HTTP/1.1\\r\\nHost: example.org\\r\\n\\r\\n")
    >>>     mock_response(http, b"HTTP/1.1 200 OK\\r\\nContent-Type: text/html\\r\\n\\r\\nHello world")
    >>>     assert_remote_write(http, b"GET / HTTP/1.1\\r\\nHost: example.org\\r\\n\\r\\n")

The following helpers are available for testing protocols:
"""


from pont.flow import Flow
from pont.protocols.protocol import Protocol
from pont.tests.protocols.mock import MockTransport


def assert_remote_connect(protocol: Protocol, host: str, port: int):
    """
    Assert that the connection to the remote server has been made
    with the correct host and port

    Args:
        protocol: The protocol instance
        host: The remote host we should connect to
        port: The remote port we should connect to

    Examples:
        >>> assert_remote_connect(protocol, "example.org", 80)
    """
    protocol.remote_connect.assert_called_once_with(host, port)  # type: ignore (Protocol has no method assert_called_once_with)


def assert_remote_ssl_connect(protocol: Protocol, host: str, port: int):
    """
    Assert that the SSL connection to the remote server has been made
    with the correct host and port

    Args:
        protocol: The protocol instance
        host: The remote host we should connect to
        port: The remote port we should connect to

    Examples:
        >>> assert_remote_ssl_connect(protocol, "example.org", 443)
    """
    protocol.remote_ssl_connect.assert_called_once_with(host, port)  # type: ignore (Protocol has no method assert_called_once_with)


def assert_remote_write(protocol: Protocol, data: bytes):
    """
    Assert that the data has been written to the remote server

    Args:
        protocol: The protocol instance
        data: The data that should have been written

    Examples:
        >>> assert_remote_write(protocol, b"GET / HTTP/1.1\\r\\nHost: example.org\\r\\n\\r\\n")
    """
    if isinstance(protocol._remote_transport, MockTransport):
        assert protocol._remote_transport.buffer == data
    else:
        raise Exception("The remote transport is not a mock transport")


def assert_client_write(protocol: Protocol, data: bytes):
    """
    Assert that the data has been written to the client

    Args:
        protocol: The protocol instance
        data: The data that should have been written

    Examples:
        >>> assert_client_write(protocol, b"HTTP/1.1 200 OK\\r\\nContent-Type: text/html\\r\\n\\r\\nHello world")
    """
    if isinstance(protocol._client_transport, MockTransport):
        assert protocol._client_transport.buffer == data
    else:
        raise Exception("The client transport is not a mock transport")


def mock_request(protocol: Protocol, request: bytes) -> Flow:
    """
    Mock a request from the client and call the protocol methods to parse it

    Args:
        protocol: The protocol instance
        request: The raw request

    Examples:
        >>> mock_request(protocol, b"GET / HTTP/1.1\\r\\nHost: example.org\\r\\n\\r\\n")
    """

    protocol.client_data_received(request)
    protocol.client_buffer_updated()
    return protocol.current_flow()


def mock_response(protocol: Protocol, response: bytes) -> Flow:
    """
    Mock a response from the remote server and call the protocol methods to parse it

    Args:
        protocol: The protocol instance
        response: The raw response

    Examples:
        >>> mock_response(protocol, b"HTTP/1.1 200 OK\\r\\nContent-Type: text/html\\r\\n\\r\\nHello world")
    """
    protocol.remote_data_received(response)
    protocol.remote_buffer_updated()
    return protocol.current_flow()
