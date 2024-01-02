import asyncio


class MockTransport(asyncio.Transport):
    """
    A mock transport that can be used to intercept data written to it
    """

    buffer: bytes
    # A buffer to store the data written to the transport and access it into the tests

    def __init__(self):
        self.buffer = b""

    def write(self, data: bytes):
        self.buffer += data
