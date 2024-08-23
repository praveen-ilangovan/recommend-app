"""
Test the Users collection
"""

# PyTest imports
import pytest

# Package imports
from recommend_app.db.recommendDB import RecommendDB
from recommend_app.db.exceptions import RecommendDBDuplicateKeyError

TEST_USER_EMAIL = 'testUser123@example.com'

def test_add_user(recommendDB):
    assert recommendDB.add_user(TEST_USER_EMAIL)

def test_add_duplicate_user(recommendDB):
    recommendDB.add_user('testUser124@example.com')
    with pytest.raises(RecommendDBDuplicateKeyError):
        recommendDB.add_user('testUser124@example.com')
