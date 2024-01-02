import typing

import pytest

from pont.database.database import Database
from pont.protocols.protocol import Protocol

from .mock import MockTransport


@pytest.fixture
def database() -> Database:
    return Database()


@pytest.fixture
def create_protocol(database: Database, mocker):
    """
    Pytest fixture to for creation a protocol instance for tests with proper mocks to
    intercept network calls

    Examples:
        >>> def test_parse_http11_get(create_protocol):
        >>>     http = create_protocol(HTTP)
    """

    def _method(protocol_class: typing.Type[Protocol]) -> Protocol:
        protocol = protocol_class(database)
        protocol._client_transport = MockTransport()
        protocol._remote_transport = MockTransport()
        mock = mocker.patch.object(protocol, "remote_connect")
        mock.side_effect = lambda *args: protocol.remote_connection_made()
        mock = mocker.patch.object(protocol, "remote_ssl_connect")
        mock.side_effect = lambda *args: protocol.remote_ssl_connection_made()
        protocol.client_connection_made()
        return protocol

    return _method


# Allow the assert failures to be correctly reported
pytest.register_assert_rewrite("pont.tests.protocols.helpers")
