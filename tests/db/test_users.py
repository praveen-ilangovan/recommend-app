"""
Test the Users collection
"""

# PyTest imports
import pytest

# Package imports
from recommend_app.db.exceptions import (RecommendDBDuplicateKeyError,
                                         RecommendDBInvalidIDError,
                                         RecommendDBObjectNotFound)


###############################################################################
# Tests
###############################################################################

def test_add_user(recommendDB):
    assert recommendDB.add_user('testUser123@example.com')

def test_add_duplicate_user(recommendDB):
    recommendDB.add_user('testUser124@example.com')
    with pytest.raises(RecommendDBDuplicateKeyError):
        recommendDB.add_user('testUser124@example.com')

def test_get_user(recommendDB):
    user_id = recommendDB.add_user('testUser125@example.com')
    user = recommendDB.get_user(user_id)
    assert user.email_address == 'testUser125@example.com'

def test_get_user_invalid_id_type(recommendDB):
    with pytest.raises(RecommendDBInvalidIDError):
        recommendDB.get_user(1234)

def test_get_user_invalid_id_length(recommendDB):
    with pytest.raises(RecommendDBInvalidIDError):
        recommendDB.get_user('634556')

def test_get_user_who_doesnt_exist(recommendDB):
    with pytest.raises(RecommendDBObjectNotFound):
        recommendDB.get_user('111111111111111111111111')
