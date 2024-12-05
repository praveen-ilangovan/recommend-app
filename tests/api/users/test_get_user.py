"""
Signed in user -- getting himself -> user + all boards
Signed in user -- getting a different user -> user + public boards
No signed in user -- getting a user -> user + public boards
"""

# Project specific imports
import pytest
from fastapi import status

# Local imports
from recommend_app.api import constants as Key
from recommend_app.api import auth
from recommend_app.api.app import app
from ... import utils

#-----------------------------------------------------------------------------#
# Tests
#-----------------------------------------------------------------------------#
@pytest.mark.asyncio(loop_scope="session")
async def test_get_me(api_client_with_boards):
    api_client = api_client_with_boards['api_client']
    get_user_response = await api_client.get(Key.ROUTES.GET_USER.format(user_id = '1234'))
    assert get_user_response.status_code == status.HTTP_307_TEMPORARY_REDIRECT

@pytest.mark.asyncio(loop_scope="session")
async def test_get_me_valid_user_id(api_client):
    new_user = utils.create_user()
    response = await api_client.post(Key.ROUTES.ADD_USER, json=new_user.model_dump())    
    result = response.json()

    def local_user_override():
        return auth.AuthenticatedUser(sub=result['email_address'],
                                      email_address=result['email_address'],
                                      id=result['id'],
                                      user_name=result['user_name'],
                                      first_name=result['first_name'],
                                      last_name=result['last_name'])
    
    get_authenticated_user_override = app.dependency_overrides.get(auth.get_authenticated_user)
    get_user_override = app.dependency_overrides.get(auth.get_user)

    app.dependency_overrides[auth.get_authenticated_user] = local_user_override
    app.dependency_overrides[auth.get_user] = local_user_override

    # DO your test
    get_user_response = await api_client.get(Key.ROUTES.GET_USER.format(user_id = result['id']))

    if get_authenticated_user_override:
        app.dependency_overrides[auth.get_authenticated_user] = get_authenticated_user_override
    else:
        del app.dependency_overrides[auth.get_authenticated_user]

    if get_user_override:
        app.dependency_overrides[auth.get_user] = get_user_override
    else:
        del app.dependency_overrides[auth.get_user]

    assert get_user_response.status_code == status.HTTP_307_TEMPORARY_REDIRECT

@pytest.mark.asyncio(loop_scope="session")
async def test_get_different_user(api_client):
    new_user = utils.create_user()
    response = await api_client.post(Key.ROUTES.ADD_USER, json=new_user.model_dump())    
    result = response.json()

    def local_user_override():
        return auth.AuthenticatedUser(sub=result['email_address'],
                                      email_address=result['email_address'],
                                      id=result['id'],
                                      user_name=result['user_name'],
                                      first_name=result['first_name'],
                                      last_name=result['last_name'])
    
    get_authenticated_user_override = app.dependency_overrides.get(auth.get_authenticated_user)
    get_user_override = app.dependency_overrides.get(auth.get_user)

    app.dependency_overrides[auth.get_authenticated_user] = local_user_override
    app.dependency_overrides[auth.get_user] = local_user_override

    # DO your test
    for _ in range(3):
        await api_client.post(Key.ROUTES.ADD_BOARD, json=utils.create_public_board().model_dump())
    for _ in range(2):
        await api_client.post(Key.ROUTES.ADD_BOARD, json=utils.create_private_board().model_dump())

    app.dependency_overrides[auth.get_authenticated_user] = utils.get_fake_user
    app.dependency_overrides[auth.get_user] = utils.get_fake_user
    get_user_response = await api_client.get(Key.ROUTES.GET_USER.format(user_id = result['id']))

    if get_authenticated_user_override:
        app.dependency_overrides[auth.get_authenticated_user] = get_authenticated_user_override
    else:
        del app.dependency_overrides[auth.get_authenticated_user]

    if get_user_override:
        app.dependency_overrides[auth.get_user] = get_user_override
    else:
        del app.dependency_overrides[auth.get_user]

    assert get_user_response.status_code == status.HTTP_200_OK

    user_with_boards = get_user_response.json()
    assert user_with_boards['user']['id'] == result['id']
    assert len(user_with_boards['boards']) == 3

@pytest.mark.asyncio(loop_scope="session")
async def test_get_user_no_signin(api_client):
    new_user = utils.create_user()
    response = await api_client.post(Key.ROUTES.ADD_USER, json=new_user.model_dump())    
    result = response.json()

    def local_user_override():
        return auth.AuthenticatedUser(sub=result['email_address'],
                                      email_address=result['email_address'],
                                      id=result['id'],
                                      user_name=result['user_name'],
                                      first_name=result['first_name'],
                                      last_name=result['last_name'])
    
    get_authenticated_user_override = app.dependency_overrides.get(auth.get_authenticated_user)
    get_user_override = app.dependency_overrides.get(auth.get_user)

    app.dependency_overrides[auth.get_authenticated_user] = local_user_override
    app.dependency_overrides[auth.get_user] = local_user_override

    # DO your test
    for _ in range(3):
        await api_client.post(Key.ROUTES.ADD_BOARD, json=utils.create_public_board().model_dump())
    for _ in range(2):
        await api_client.post(Key.ROUTES.ADD_BOARD, json=utils.create_private_board().model_dump())

    app.dependency_overrides[auth.get_authenticated_user] = utils.get_no_user
    app.dependency_overrides[auth.get_user] = utils.get_no_user
    get_user_response = await api_client.get(Key.ROUTES.GET_USER.format(user_id = result['id']))

    if get_authenticated_user_override:
        app.dependency_overrides[auth.get_authenticated_user] = get_authenticated_user_override
    else:
        del app.dependency_overrides[auth.get_authenticated_user]

    if get_user_override:
        app.dependency_overrides[auth.get_user] = get_user_override
    else:
        del app.dependency_overrides[auth.get_user]

    assert get_user_response.status_code == status.HTTP_200_OK

    user_with_boards = get_user_response.json()
    assert user_with_boards['user']['id'] == result['id']
    assert len(user_with_boards['boards']) == 3

@pytest.mark.asyncio(loop_scope="session")
async def test_get_non_existent_user(api_client_with_boards):
    api_client = api_client_with_boards['api_client']
    get_user_response = await api_client.get(Key.ROUTES.GET_USER.format(user_id = '1234567'))
    assert get_user_response.status_code == status.HTTP_404_NOT_FOUND
