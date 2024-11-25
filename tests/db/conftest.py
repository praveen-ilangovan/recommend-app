"""
Fixtures
"""

# Builtin imports
import os

# Project specific imports
import pytest_asyncio

# App specific imports
from recommend_app.db import create_client, RecommendDB

#-----------------------------------------------------------------------------#
# Fixtures
# For async: https://pytest-asyncio.readthedocs.io/en/latest/how-to-guides/run_session_tests_in_same_loop.html
#-----------------------------------------------------------------------------#

@pytest_asyncio.fixture(loop_scope="session")
async def db_client():
    client = create_client( RecommendDB(os.environ["DB_NAME"]) )
    await client.connect()

    yield client

    await client.disconnect(clear_db=True)
