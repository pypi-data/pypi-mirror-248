import aiohttp.web
import pytest
import pytest_asyncio

from pont.database import Database
from pont.settings import Settings
from pont.ui import setup_app


@pytest.fixture
def database() -> Database:
    return Database()


@pytest.fixture
def settings() -> Settings:
    return Settings()


@pytest_asyncio.fixture
async def http_server(aiohttp_client, database, settings) -> aiohttp.web.Application:
    app = setup_app()
    app["database"] = database
    app["settings"] = settings
    return await aiohttp_client(app)
