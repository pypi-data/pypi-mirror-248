# This is complex, but the core idea is that we want to create a SSL connection
# using the asyncio capatibilities provided by Python. In oder to do that we are going
# to create a wrapping server and client protocol that will handle the SSL handshake
# and then pass the data to the wrapped protocol. The goal is to be be transparent
# for upper layers.
#
import asyncio
import ssl


class SSLProxyClientProtocol(asyncio.Protocol):
    def __init__(self, proxy_transport, app_protocol):
        self.proxy_transport = proxy_transport
        self.app_protocol = app_protocol

    def connection_made(self, _remote_transport: asyncio.Transport):  # type: ignore MyPy consider we are receiving a BaseTransport
        proxy_ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        proxy_ssl_context.load_cert_chain("cert.pem")

        self._server_protocol = SSLProxyServerProtocol(self.app_protocol)

        # asyncio.sslproto.SSLProtocol is a Protocol that wrap another protocol
        # it will handle the SSL handshake and then pass the data to the wrapped protocol
        # It's an undocumented class, but it's provided by the standard library
        ssl_protocol = asyncio.sslproto.SSLProtocol(  # type: ignore
            loop=asyncio.get_running_loop(),
            app_protocol=self._server_protocol,
            sslcontext=proxy_ssl_context,
            waiter=asyncio.Future(),
            server_side=True,
        )
        self.app_protocol.remote_ssl_connection_made()
        self.proxy_transport.set_protocol(ssl_protocol)
        ssl_protocol.connection_made(self.proxy_transport)

    def data_received(self, data):
        self.app_protocol.remote_data_received(data)

    def connection_lost(self, exc: Exception | None) -> None:
        self.proxy_transport.close()


class SSLProxyServerProtocol(asyncio.Protocol):
    """
    Use once the connection is etablish to the proxy
    """

    def __init__(self, app_protocol: asyncio.Protocol):
        self.app_protocol = app_protocol

    def connection_made(self, transport: asyncio.Transport) -> None:  # type: ignore a BaseTransport is expected
        # TODO: It's not clean to access a private attribute
        self.app_protocol._client_transport = transport  # type: ignore (Access to protected attribute in the same module)

    def data_received(self, data: bytes) -> None:
        self.app_protocol.client_data_received(data)  # type: ignore (Unknow in BaseProtocol but defined in Protocol)


def create_ssl_transport_wrapper(
    host: str, port: int, transport: asyncio.Transport, app_protocol
) -> None:
    """
    Wrapper to create a SSL transport that will decode the content
    Args:
        host: The remote host
        port: The remote port
    """
    loop = asyncio.get_running_loop()

    print("Connect to the remote server with SSL to %s:%s" % (host, port))
    coro = loop.create_connection(
        lambda: SSLProxyClientProtocol(transport, app_protocol),
        host,
        port,
        ssl=ssl.create_default_context(),
    )
    asyncio.ensure_future(coro)
