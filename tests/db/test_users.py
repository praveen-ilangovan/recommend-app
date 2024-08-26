"""
Test the Users collection
"""

# PyTest imports
import pytest

# Package imports
from recommend_app.db_client.models.user import User
from recommend_app.db_client.exceptions import (RecommendDBModelCreationError,
                                                RecommendDBModelNotFound)


###############################################################################
# Tests
###############################################################################

def test_add_user(recommendDBClient):
    assert recommendDBClient.add_user('testUser1@example.com')

def test_add_user_rtype(recommendDBClient):
    user = recommendDBClient.add_user('testUser2@example.com')
    assert isinstance(user, User)
    assert user.email_address == 'testUser2@example.com'

def test_add_duplicate_user(recommendDBClient):
    recommendDBClient.add_user('testUser124@example.com')
    with pytest.raises(RecommendDBModelCreationError):
        recommendDBClient.add_user('testUser124@example.com')

def test_get_user(recommendDBClient):
    user = recommendDBClient.add_user('testUser125@example.com')
    user1 = recommendDBClient.get_user(user.uid)
    assert user1.email_address == 'testUser125@example.com'

def test_get_user_invalid_id_type(recommendDBClient):
    with pytest.raises(RecommendDBModelNotFound):
        recommendDBClient.get_user(1234)

def test_get_user_invalid_id_length(recommendDBClient):
    with pytest.raises(RecommendDBModelNotFound):
        recommendDBClient.get_user('634556')

def test_get_user_who_doesnt_exist(recommendDBClient):
    with pytest.raises(RecommendDBModelNotFound):
        recommendDBClient.get_user('111111111111111111111111')

def test_get_user_by_email_address(recommendDBClient):
    email_address = 'testUser126@example.com'
    user1 = recommendDBClient.add_user(email_address)
    user2 = recommendDBClient.get_user_by_email_address(email_address)
    assert user1.email_address == email_address
    assert user2.uid == user1.uid
    assert user1 == user2

def test_get_user_by_invalid_email_address(recommendDBClient):
    with pytest.raises(RecommendDBModelNotFound):
        recommendDBClient.get_user_by_email_address("invalidemailid")

def test_remove_user(recommendDBClient):
    user = recommendDBClient.add_user("test1219@example.com")
    assert recommendDBClient.remove_user(user)

def test_remove_user_non_existent_user(recommendDBClient):
    user = User(email_address='t@eple.com', uid='66c9fa30ead0ee3fdef76ad2')
    assert not recommendDBClient.remove_user(user)
