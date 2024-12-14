"""
Testing extension routes
"""

# Builtin imports
import json
from datetime import timedelta

# Project specific imports
import pytest
from fastapi import status

# Local imports
from recommend_app.api.routers.extension import reissue_token, AuthenticatedUserWithToken
from recommend_app.api import constants, auth

from .. import utils

class FakeRequest:
    headers = {}

def get_authdata(user=None, create_token=False):
    user = user or utils.get_fake_user()
    headers_dict = {**user.model_dump()}
    if not create_token:
        headers_dict['access_token'] = '1234'
    else:
        access_token_expires = timedelta(minutes=constants.ACCESS_TOKEN_EXPIRE_MINUTES)
        token = auth.create_access_token(user, access_token_expires)
        headers_dict['access_token'] = token.access_token

    return headers_dict

def get_request(authdata):
    request = FakeRequest()
    request.headers = {'UserAuthData' : json.dumps(authdata)}
    return request

#-----------------------------------------------------------------------------#
# Tests
#-----------------------------------------------------------------------------#

def test_reissue_token_with_access_token():
    authdata = get_authdata(create_token=True)
    request = get_request(authdata)

    result = reissue_token(request)
    assert isinstance(result, AuthenticatedUserWithToken)
    assert result.access_token == authdata['access_token']


def test_reissue_token_without_access_token():
    authdata = get_authdata(create_token=False)
    request = get_request(authdata)

    result = reissue_token(request)
    assert isinstance(result, AuthenticatedUserWithToken)
    assert result.access_token

@pytest.mark.asyncio(loop_scope="session")
async def test_create_access_token(api_client_with_boards):
    api_client = api_client_with_boards['api_client']

    new_user = utils.create_user()
    password = new_user.password

    # Create a user
    await api_client.post(constants.ROUTES.ADD_USER, json=new_user.model_dump())

    # Login
    response = await api_client.post(constants.ROUTES.CREATE_TOKEN,
                               data={"username": new_user.user_name,
                                     "password": password,
                                     "grant_type": "password"},
                               headers={"content-type": "application/x-www-form-urlencoded"})
    result = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert result['user_name'] == new_user.user_name
    assert result['access_token']

@pytest.mark.asyncio(loop_scope="session")
async def test_create_access_token_invalid_password(api_client_with_boards):
    api_client = api_client_with_boards['api_client']

    new_user = utils.create_user()
    password = new_user.password

    # Create a user
    await api_client.post(constants.ROUTES.ADD_USER, json=new_user.model_dump())

    # Login
    response = await api_client.post(constants.ROUTES.CREATE_TOKEN,
                               data={"username": new_user.user_name,
                                     "password": 'test',
                                     "grant_type": "password"},
                               headers={"content-type": "application/x-www-form-urlencoded"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.asyncio(loop_scope="session")
async def test_get_verified_user(api_client_with_boards):
    api_client = api_client_with_boards['api_client']

    authdata = get_authdata(create_token=True)
    request = get_request(authdata)

    response = await api_client.get(constants.ROUTES.GET_VERIFIED_USER,
                                    headers = request.headers)
    result = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert result['user']['id'] == '1234'
    assert result['boards']

@pytest.mark.asyncio(loop_scope="session")
async def test_get_verified_user_with_no_headers(api_client_with_boards):
    api_client = api_client_with_boards['api_client']
    response = await api_client.get(constants.ROUTES.GET_VERIFIED_USER)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.asyncio(loop_scope="session")
async def test_add_card(api_client_with_boards):
    api_client = api_client_with_boards['api_client']
    board = api_client_with_boards['public_board']

    authdata = get_authdata(create_token=True)
    request = get_request(authdata)
    new_card = utils.create_card()

    response = await api_client.post(constants.ROUTES.ADD_CARD_FROM_EXTN.format(board_id=board['id']),
                                     json=new_card.model_dump(),
                                     headers = request.headers)
    result = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    assert result['title'] == new_card.title
