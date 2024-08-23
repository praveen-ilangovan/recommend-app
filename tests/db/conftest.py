# PyTest imports
import pytest

# Package imports
from recommend_app.db.recommendDB import RecommendDB

TEST_DB_NAME = 'testRecommendDB'

###############################################################################
# Fixtures
###############################################################################
@pytest.fixture(scope="module")
def recommendDB():
    db = RecommendDB.connect(TEST_DB_NAME)

    yield db

    # Cleanup
    db._db.client.drop_database(TEST_DB_NAME)
