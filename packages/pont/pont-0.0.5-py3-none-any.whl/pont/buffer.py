class Buffer:
    """
    Wrapper around a byte buffer providing useful methods
    """

    def __init__(self) -> None:
        self._buf = b""

    def write(self, data: bytes) -> None:
        """
        Append data to the buffer
        """
        self._buf += data

    def read_until(self, delimiter: bytes) -> bytes | None:
        """
        Read until the delimiter is found
        """
        if delimiter in self._buf:
            data, self._buf = self._buf.split(delimiter, 1)
            return data
        return None

    def read(self) -> bytes:
        """
        Read the whole buffer
        """
        data = self._buf
        self._buf = b""
        return data

    def __len__(self) -> int:
        return len(self._buf)

    def __str__(self) -> str:
        return self._buf.decode()
