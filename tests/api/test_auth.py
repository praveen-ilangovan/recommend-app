"""
Test the auth module. creating and decoding access tokens
"""

# Builtin imports
from datetime import timedelta

# Project specific imports
import pytest

# Local imports
from recommend_app.api import auth

from .. import utils

@pytest.fixture()
def authenticated_user():
    user = utils.create_user()
    return auth.AuthenticatedUser(sub=user.email_address,
                                  email_address=user.email_address,
                                  user_name=user.email_address,
                                  first_name=user.first_name,
                                  last_name=user.last_name,
                                  id="TempID")

#-----------------------------------------------------------------------------#
# Test
#-----------------------------------------------------------------------------#

def test_access_token(authenticated_user):
    access_token_expires = timedelta(minutes=1)
    token = auth.create_access_token(authenticated_user, access_token_expires)
    assert isinstance(token, auth.Token)
    assert token.name == auth.OAUTH2_SCHEME.token_name

    user = auth._decode_token(token.access_token)
    assert user == authenticated_user

def test_invalid_access_token():
    user = auth._decode_token("MyInvalidAccessToken")
    assert not user
