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

class FakeRequest:
    headers = {}
    cookies = {}

#-----------------------------------------------------------------------------#
# Fixtures
#-----------------------------------------------------------------------------#

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
    assert user.email_address == authenticated_user.email_address

def test_invalid_access_token():
    user = auth._decode_token("MyInvalidAccessToken")
    assert not user

#-----------------------------------------------------------------------------#
# Get token from header
#-----------------------------------------------------------------------------#
@pytest.mark.asyncio(loop_scope="session")
async def test_get_token_from_header():
    request = FakeRequest()
    request.headers = {"Authorization": "Bearer test123",
                       "Content-Type": "application/json"}
    result = await auth.get_token_from_header(request)
    assert result == 'test123'

@pytest.mark.asyncio(loop_scope="session")
async def test_get_token_from_header_no_auth():
    request = FakeRequest()
    request.headers = {}
    result = await auth.get_token_from_header(request)
    assert not result

@pytest.mark.asyncio(loop_scope="session")
async def test_get_token_from_header_no_bearer():
    request = FakeRequest()
    request.headers = {"Authorization": "test123",
                       "Content-Type": "application/json"}
    result = await auth.get_token_from_header(request)
    assert not result

@pytest.mark.asyncio(loop_scope="session")
async def test_get_token_from_header_undefined():
    request = FakeRequest()
    request.headers = {"Authorization": "Bearer undefined",
                       "Content-Type": "application/json"}
    result = await auth.get_token_from_header(request)
    assert not result

#-----------------------------------------------------------------------------#
# Get from cookies
#-----------------------------------------------------------------------------#
def test_get_token_from_cookies():
    request = FakeRequest()
    request.cookies = {"access_token": "test123"}
    result = auth.get_token_from_cookie(request, "access_token")
    assert result == 'test123'

def test_get_token_from_cookies_no_token():
    request = FakeRequest()
    result = auth.get_token_from_cookie(request, "access_token")
    assert not result

#-----------------------------------------------------------------------------#
# Test OAUTH2_SCHEME
#-----------------------------------------------------------------------------#
@pytest.mark.asyncio(loop_scope="session")
async def test_OAUTH2_SCHEME_auth_header():
    request = FakeRequest()
    request.headers = {"Authorization": "Bearer header_token",
                       "Content-Type": "application/json"}
    request.cookies = {"access_token": "cookie_token"}
    result = await auth.OAUTH2_SCHEME(request)
    assert result == "header_token"

@pytest.mark.asyncio(loop_scope="session")
async def test_OAUTH2_SCHEME_cookie_fallback():
    request = FakeRequest()
    request.headers = {"Authorization": "header_token",
                       "Content-Type": "application/json"}
    request.cookies = {"access_token": "cookie_token"}
    result = await auth.OAUTH2_SCHEME(request)
    assert result == "cookie_token"

@pytest.mark.asyncio(loop_scope="session")
async def test_OAUTH2_SCHEME_no_token_atall():
    request = FakeRequest()
    request.headers = {"Authorization": "header_token",
                       "Content-Type": "application/json"}
    request.cookies = {"accesstoken": "cookie_token"}
    result = await auth.OAUTH2_SCHEME(request)
    assert not result
