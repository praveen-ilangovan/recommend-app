"""
Test connecting to the db
"""

# Project specific imports
import pytest

#-----------------------------------------------------------------------------#
# Tests
#-----------------------------------------------------------------------------#

@pytest.mark.asyncio(loop_scope="session")
async def test_db_connection(db_client):
    status = await db_client.ping()
    assert status
