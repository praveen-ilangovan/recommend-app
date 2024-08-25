"""
Test the user model
"""

# PyTest imports
import pytest

# Package imports
from recommend_app.db_client.models.user import User

TEST_EMAIL_ADDRESS = 'thisCoulcBeAnything@gmail.com'

###############################################################################
# Fixtures
###############################################################################
@pytest.fixture(scope="module")
def user():
    return User(TEST_EMAIL_ADDRESS)

###############################################################################
# Tests
###############################################################################

def test_user_creation(user):
    assert isinstance(user, User)

def test_user_email_address(user):
    assert user.email_address == TEST_EMAIL_ADDRESS

def test_user_comparison(user):
    user2 = User('thisCoulcBeAnything@gmail.com')
    assert user == user2

