from typing import Tuple

from .protocol import Protocol

STATE_PARSE_METHOD = 0
STATE_PARSE_PATH = 1
STATE_PARSE_VERSION = 2
STATE_PARSE_HEADERS = 3
STATE_PARSE_BODY = 4
STATE_PARSE_STATUS = 5
# Special state for HTTPS, after the CONNECT method
# we will get back to the state STATE_PARSE_METHOD at the end of the handshake
STATE_SSL_HANDSHAKE = 6


class HTTP(Protocol):
    _client_buffer: bytes
    _client_state: int
    _remote_state: int

    def client_connection_made(self) -> None:
        self._client_state = STATE_PARSE_METHOD
        self._remote_state = STATE_PARSE_VERSION
        self._client_headers = {}

    def remote_ssl_connection_made(self) -> None:
        self.client_write(b"HTTP/1.1 200 OK\r\n\r\n")
        self.client_connection_made()

    def remote_connection_made(self) -> None:
        connection = f"{self.current_flow().method} {self.current_flow().path}"
        if self.current_flow().query:
            connection += f"?{self.current_flow().query}"
        connection += " HTTP/1.1\r\n"
        for key, value in self.current_flow().request_headers.items():
            connection += f"{key}: {value}\r\n"
        connection += "\r\n"
        self.remote_write(connection.encode())

    def remote_buffer_updated(self) -> None:
        if self._remote_state == STATE_PARSE_VERSION:
            version = self.remote_buffer.read_until(b" ")
            if version:
                self._remote_state = STATE_PARSE_STATUS
                self.client_write(version)
                self.client_write(b" ")
        elif self._remote_state == STATE_PARSE_STATUS:
            status = self.remote_buffer.read_until(b"\r\n")
            if status:
                self.current_flow().status = status.decode()
                self._remote_state = STATE_PARSE_HEADERS
                self.client_write(status)
                self.client_write(b"\r\n")
        elif self._remote_state == STATE_PARSE_HEADERS:
            line = self.remote_buffer.read_until(b"\r\n")
            if line is not None:
                self.client_write(line)
                self.client_write(b"\r\n")
                # End of headers
                if len(line) == 0:
                    self._remote_state = STATE_PARSE_BODY
                else:
                    key, value = self._parse_header_line(line)
                    self.current_flow().response_headers[key] = value
        elif self._remote_state == STATE_PARSE_BODY:
            data = self.remote_buffer.read()
            if self.current_flow().response_headers["Content-Type"]:
                self.current_flow().response_mime_type = (
                    self.current_flow().response_headers["Content-Type"].split(";")[0]
                )
            self.client_write(data)
            self.current_flow().response_body += data

    def client_buffer_updated(self) -> None:
        if self._client_state == STATE_PARSE_METHOD:
            method = self.client_buffer.read_until(b" ")
            if method == b"CONNECT":
                self.new_flow("https").method = method.decode()
            elif method:
                self.new_flow("http").method = method.decode()
            self._client_state = STATE_PARSE_PATH
        elif self._client_state == STATE_PARSE_PATH:
            path = self.client_buffer.read_until(b" ")
            if path:
                self._parse_path(path.decode())
                self._client_state = STATE_PARSE_VERSION
        elif self._client_state == STATE_PARSE_VERSION:
            version = self.client_buffer.read_until(b"\r\n")
            if version:
                self._client_state = STATE_PARSE_HEADERS
        elif self._client_state == STATE_PARSE_HEADERS:
            line = self.client_buffer.read_until(b"\r\n")
            if line is not None:
                # End of headers
                if len(line) == 0:
                    self._header_parsed()
                else:
                    key, value = self._parse_header_line(line)
                    self.current_flow().request_headers[key] = value
        elif self._client_state == STATE_PARSE_BODY:
            data = self.client_buffer.read()
            self.current_flow().request_body += data
            self.remote_write(data)

    def _header_parsed(self):
        """
        Called when the headers have been parsed
        """
        flow = self.current_flow()
        if flow.protocol == "http":
            self._client_state = STATE_PARSE_BODY
            # TODO: Handle is Host is not present
            # TODO: get port
            flow.host = self.current_flow().request_headers["Host"]
            flow.port = 80
            self.remote_connect(flow.host, flow.port)
        else:
            self._client_state = STATE_SSL_HANDSHAKE
            if ":" in self.current_flow().path:
                flow.host, port = self.current_flow().path.split(":", 1)
                flow.port = int(port)
            else:
                flow.host = self.current_flow().path
                flow.port = 443
            self.remote_ssl_connect(flow.host, flow.port)

    def _parse_path(self, path: str):
        """
        Extract the path and the query string from the path
        """
        if "?" in path:
            path, query = path.split("?", 1)
            self.current_flow().query = query

        # Remove the host if present
        if path.startswith("http://"):
            path = path[7:]
            path = path[path.find("/") :]

        self.current_flow().path = path

    def _parse_header_line(self, line) -> Tuple[str, str]:
        key, value = line.split(b":", 1)
        # TODO: Make it case insensitive and handle errors
        value = value.decode().rstrip().strip()
        return (key.decode(), value)
