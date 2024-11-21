# Builtin imports
import time

# PyTest imports
import pytest

# Package imports
from recommend_app.db_client import create_client
from recommend_app.db_async_impl import create_aysnc_db

TEST_DB_NAME = 'asyncTestRecommendDB'

###############################################################################
# Fixtures
###############################################################################
@pytest.fixture(scope="module")
def recommendDBClient():
    db = create_aysnc_db(TEST_DB_NAME)
    client = create_client(db)
    client.connect()

    yield client

    # Cleanup
    db._db.client.drop_database(TEST_DB_NAME)
