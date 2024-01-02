# This is complex, but the core idea is that we want to create a SSL connection
# using the asyncio capatibilities provided by Python. In oder to do that we are going
# to create a wrapping server and client protocol that will handle the SSL handshake
# and then pass the data to the wrapped protocol. The goal is to be be transparent
# for upper layers.
#
import asyncio
import datetime
import logging
import ssl

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID

from ..settings import Settings


def generate_certificate(key_size=4096):
    """
    Generate a self signed certificate.

    Args:
        key_size: The key size in bits. Default is 4096.
    Returns:
        The certificate as a PEM encoded string.
    """
    key = rsa.generate_private_key(
        public_exponent=65537, key_size=key_size, backend=default_backend()
    )

    name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "pont")])

    cert = (
        x509.CertificateBuilder()
        .subject_name(name)
        .issuer_name(name)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.datetime.utcnow())
        .not_valid_after(
            # Our certificate will be valid for 10 years
            datetime.datetime.utcnow() + datetime.timedelta(days=365 * 10)
        )
        .sign(key, hashes.SHA256(), default_backend())
    )
    cert_pem = cert.public_bytes(encoding=serialization.Encoding.PEM)
    key_pem = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    )

    return key_pem + cert_pem


class Certificate:
    _cert_path = None

    @classmethod
    def get(cls):
        """
        Get the certificate from the settings directory or generate a new one.

        Returns:
            The certificate as a PEM encoded string.
        """

        if cls._cert_path is not None:
            return cls._cert_path

        # TODO: This is not clean, we should not access have to reload the settings
        settings = Settings()
        settings.load()
        cls._cert_path = settings.config_directory() / "cert.pem"
        if cls._cert_path.exists():
            return cls._cert_path
        else:
            logging.info(f"Generating a new certificate in {cls._cert_path }")
            cert = generate_certificate()
            with cls._cert_path.open("wb") as file:
                file.write(cert)
            return cls._cert_path


class SSLProxyClientProtocol(asyncio.Protocol):
    def __init__(self, proxy_transport, app_protocol):
        self.proxy_transport = proxy_transport
        self.app_protocol = app_protocol

    def connection_made(self, _remote_transport: asyncio.Transport):  # type: ignore MyPy consider we are receiving a BaseTransport
        proxy_ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        proxy_ssl_context.load_cert_chain(Certificate.get())

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

    coro = loop.create_connection(
        lambda: SSLProxyClientProtocol(transport, app_protocol),
        host,
        port,
        ssl=ssl.create_default_context(),
    )
    asyncio.ensure_future(coro)
