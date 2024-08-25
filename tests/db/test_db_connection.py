"""
Test the recommendDB
"""

# Builtin imports
import os

# PyTest imports
import pytest

# Package imports
from recommend_app.db_client import create_client
from recommend_app.db_impl import create_db
from recommend_app.db_client.client import RecommendDbClient
from recommend_app.db_client.exceptions import RecommendDBConnectionError

TEST_DB_NAME = 'testRecommendDB'

###############################################################################
# Fixtures
###############################################################################
@pytest.fixture(scope="function")
def invalidURL():
    right_url = os.environ['DB_URL']
    timeout = os.getenv('DB_SERVERSELECTIONTIMEOUT')
    os.environ['DB_URL'] = 'myInvalidMongoDB'
    os.environ['DB_SERVERSELECTIONTIMEOUT'] = '1'

    yield

    # cleanup
    os.environ['DB_URL'] = right_url
    if timeout is None:
        del os.environ['DB_SERVERSELECTIONTIMEOUT']
    else:
        os.environ['DB_SERVERSELECTIONTIMEOUT'] = timeout

###############################################################################
# Tests
###############################################################################
def test_db_connection_with_invalid_url(invalidURL):
    with pytest.raises(RecommendDBConnectionError):
        db = create_db("InvalidDBForTesting")
        client = create_client(db)
        client.connect()

def test_db_connection(recommendDBClient):
    assert isinstance(recommendDBClient, RecommendDbClient)
