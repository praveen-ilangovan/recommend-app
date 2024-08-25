# PyTest imports
import pytest

# Package imports
from recommend_app.db_client import create_client
from recommend_app.db_impl import create_db

TEST_DB_NAME = 'testRecommendDB'

###############################################################################
# Fixtures
###############################################################################
@pytest.fixture(scope="module")
def recommendDBClient():
    db = create_db(TEST_DB_NAME)
    client = create_client(db)
    client.connect()

    yield client

    # Cleanup
    db._db.client.drop_database(TEST_DB_NAME)
