import asyncio
import logging

from .database.database import Database
from .protocols.protocol import ClientWrapperProtocol, Protocol
from .settings import ProxySettings


class Proxy:
    database: Database
    logger: logging.Logger
    # The port to listen on

    def __init__(
        self, database: Database, settings: ProxySettings, protocol: type[Protocol]
    ) -> None:
        self.database = database
        self.logger = logging.getLogger(self.__class__.__name__)
        self._protocol = protocol
        self._settings = settings

    async def start(self) -> None:
        protocol = self._protocol(self.database)
        self.logger.info(
            f"Listening for protocol {protocol} on {self._settings.local_host}:{self._settings.local_port}"
        )

        loop = asyncio.get_running_loop()
        self._server = await loop.create_server(
            lambda: ClientWrapperProtocol(protocol),
            self._settings.local_host,
            self._settings.local_port,
        )
        await self._server.start_serving()
