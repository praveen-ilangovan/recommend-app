
# Builtin imports
import os

# Project specific imports
import pytest_asyncio
import httpx
from asgi_lifespan import LifespanManager

# Local imports
from recommend_app.api.app import app, get_db_client
from recommend_app.db import create_client, RecommendDB

#-----------------------------------------------------------------------------#
# Session Scoped Fixtures
#
# For async: https://pytest-asyncio.readthedocs.io/en/latest/how-to-guides/run_session_tests_in_same_loop.html
#-----------------------------------------------------------------------------#

@pytest_asyncio.fixture(loop_scope="session")
async def db_client():
    """
    A fixture that yields the DB client
    """
    client = create_client( RecommendDB(os.environ["DB_NAME"]) )
    await client.connect()

    yield client

    await client.disconnect(clear_db=True)


@pytest_asyncio.fixture(loop_scope="session")
async def WrappedApp(db_client):
    """
    App relies on lifespan events and the AsyncClient doesn't trigger them.
    To ensure they are triggered, use LifespanManager from florimondmanca/asgi-lifespan.

    App takes in the db_client as an input and overrides the db dependency with
    this one.
    """
    app.dependency_overrides[get_db_client] = db_client

    async with LifespanManager(app) as manager:
        yield manager.app

@pytest_asyncio.fixture(loop_scope="session")
async def api_client(WrappedApp):
    """
    The test client we will using in the test. It takes in the wrapped app along
    with the db override.
    """
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=WrappedApp), base_url="http://test") as client:
        yield client
