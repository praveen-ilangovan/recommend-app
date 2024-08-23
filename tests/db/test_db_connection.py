"""
Test the recommendDB
"""

# Builtin imports
import os

# PyTest imports
import pytest

# Package imports
from recommend_app.db.recommendDB import RecommendDB
from recommend_app.db.exceptions import RecommendDBConnectionError

TEST_DB_NAME = 'testRecommendDB'

###############################################################################
# Fixtures: With invalid env variables
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
        RecommendDB.connect(TEST_DB_NAME)

def test_db_connection(recommendDB):
    assert isinstance(recommendDB, RecommendDB)
