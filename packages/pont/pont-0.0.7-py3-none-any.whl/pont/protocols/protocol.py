import asyncio

from ..buffer import Buffer
from ..database.database import Database
from ..flow import Flow
from .ssl import create_ssl_transport_wrapper  # type: ignore (Partialy unknown)


class Protocol:
    """
    Base TCP protocol
    """

    _client_transport: asyncio.Transport
    # The transport to communicate with the client
    _remote_transport: asyncio.Transport
    # The transport to communicate with the remote server
    client_buffer: Buffer
    # Buffer storing the data received from the client
    remote_buffer: Buffer
    # Buffer storing the data received from the remote server
    _current_flow: Flow | None
    # The current flow

    def __init__(self, database: Database):
        self._database = database
        self.client_buffer = Buffer()
        self.remote_buffer = Buffer()
        self._current_flow = None

    def current_flow(self) -> Flow:
        """
        Return the current flow, a freshly created one if none exists
        """
        return self._current_flow or self.new_flow("tcp")

    def new_flow(self, protocol: str) -> Flow:
        """
        Create a new flow and add it to the database

        :param protocol: The protocol of the flow
        """
        self._current_flow = Flow(protocol)
        self._database.flows().add(self._current_flow)
        return self._current_flow

    def remote_connect(self, host: str, port: int) -> None:
        """
        Connect to the remote server
        """
        loop = asyncio.get_running_loop()
        coro = loop.create_connection(lambda: ServerWrapperProtocol(self), host, port)
        asyncio.ensure_future(coro)

    def remote_ssl_connect(self, host: str, port: int) -> None:
        """
        Connect to the remote server using SSL
        """
        create_ssl_transport_wrapper(host, port, self._client_transport, self)

    def remote_ssl_connection_made(self) -> None:
        pass

    def remote_connection_made(self) -> None:
        """
        Connection made to the remote server
        """
        pass

    def client_connection_made(self) -> None:
        """
        Connection made by the client
        """
        pass

    def client_data_received(self, data: bytes) -> None:
        """
        Data received from the client
        """
        self.client_buffer.write(data)
        len_buffer_before = len(self.client_buffer)
        self.client_buffer_updated()
        # If the buffer has been updated, we need to call the method again
        # to process the remaining data
        if len_buffer_before != len(self.client_buffer):
            self.client_data_received(b"")

    def client_buffer_updated(self) -> None:
        """
        The client buffer has been updated
        """
        raise NotImplementedError

    def remote_data_received(self, data: bytes) -> None:
        """
        Data received from the remote server
        """
        self.remote_buffer.write(data)
        len_buffer_before = len(self.remote_buffer)
        self.remote_buffer_updated()
        # If the buffer has been updated, we need to call the method again
        # to process the remaining data
        if len_buffer_before != len(self.remote_buffer):
            self.remote_data_received(b"")

    def remote_buffer_updated(self) -> None:
        """
        The remote buffer has been updated
        """
        raise NotImplementedError

    def remote_write(self, data: bytes) -> None:
        """
        Non blocking write data to the remote server
        """
        if len(data) > 0:
            self._remote_transport.write(data)

    def client_write(self, data: bytes) -> None:
        """
        Non blocking write data to the client
        """
        self._client_transport.write(data)

    def __str__(self) -> str:
        return self.__class__.__name__


class ClientWrapperProtocol(asyncio.Protocol):
    """
    Wrap the communication from the client to the server protoco

    For internal use only
    """

    def __init__(self, protocol: Protocol):
        self.protocol = protocol

    def connection_made(self, transport: asyncio.Transport):  # type: ignore (Access to protected attribute in the same module)
        self.protocol._client_transport = transport  # type: ignore (Access to protected attribute in the same module)
        self.protocol.client_connection_made()

    def data_received(self, data: bytes) -> None:
        self.protocol.client_data_received(data)


class ServerWrapperProtocol(asyncio.Protocol):
    """
    Wrap the communication from the remote server to the proxy protocol

    For internal use only
    """

    def __init__(self, protocol: Protocol):
        self.protocol = protocol

    def connection_made(self, transport: asyncio.Transport):  # type: ignore (Access to protected attribute in the same module)
        self.protocol._remote_transport = transport  # type: ignore (Access to protected attribute in the same module)
        self.protocol.remote_connection_made()

    def data_received(self, data: bytes) -> None:
        self.protocol.remote_data_received(data)
