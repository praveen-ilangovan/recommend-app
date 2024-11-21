"""
Test the user model
"""

# Builtin imports
from pydantic_core import ValidationError


# PyTest imports
import pytest

# Package imports
from recommend_app.db_client.models.user import User

# Local imports
from .. import utils

TEST_EMAIL_ADDRESS = utils.get_random_email_address()

###############################################################################
# Fixtures
###############################################################################
@pytest.fixture(scope="module")
def user():
    return User(email_address=TEST_EMAIL_ADDRESS)

###############################################################################
# Tests
###############################################################################

def test_user_creation(user):
    assert isinstance(user, User)

def test_user_invalid_email_address(user):
    with pytest.raises(ValidationError):
        User(email_address="12345.6789")

def test_user_email_address(user):
    assert user.email_address == TEST_EMAIL_ADDRESS

def test_user_immutability(user):
    with pytest.raises(ValidationError):
        user.email_address = utils.get_random_email_address()

def test_user_comparison(user):
    user2 = User(email_address=TEST_EMAIL_ADDRESS)
    assert user == user2

