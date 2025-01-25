"""
Let updating the user info

User updating their own information
User tyring to update other user's information
"""

# Project specific imports
import pytest
from fastapi import status

# Local imports
from recommend_app.api import constants as Key
from recommend_app.api.auth import AuthenticatedUser, get_authenticated_user, get_user
from recommend_app.api.app import app
from recommend_app.api import dependencies

from recommend_app.db.models.user import UpdateUser
from recommend_app.db.hashing import Hasher

from ... import utils

#-----------------------------------------------------------------------------#
# Tests
#-----------------------------------------------------------------------------#
@pytest.mark.asyncio(loop_scope="session")
async def test_update_user(api_client):
    new_user = utils.create_user()
    response = await api_client.post(Key.ROUTES.ADD_USER, json=new_user.model_dump())
    assert response.status_code == status.HTTP_201_CREATED
    created_user = response.json()

    def local_get_authenticated_user():
        return AuthenticatedUser(sub=created_user['email_address'],
                                 email_address=created_user['email_address'],
                                 id=created_user['id'],
                                 user_name=created_user['user_name'],
                                 first_name=created_user['first_name'],
                                 last_name=created_user['last_name'])
    

    get_authenticated_user_override = app.dependency_overrides.get(get_authenticated_user)
    get_user_override = app.dependency_overrides.get(get_user)
    app.dependency_overrides[get_authenticated_user] = local_get_authenticated_user
    app.dependency_overrides[get_user] = local_get_authenticated_user

    data = UpdateUser(first_name='MyFirstName', password='MySecretPassword')
    updated_response = await api_client.put(Key.ROUTES.UPDATE_USER.format(user_id=created_user['id']), json=data.model_dump())
    assert updated_response.status_code == status.HTTP_200_OK

    updated_user = await dependencies.get_db_client().get_user(created_user['id'])
    assert updated_user.first_name == data.first_name
    assert Hasher.verify_password(data.password, updated_user.password)

    if get_authenticated_user_override:
        app.dependency_overrides[get_authenticated_user] = get_authenticated_user_override
    else:
        del app.dependency_overrides[get_authenticated_user]

    if get_user_override:
        app.dependency_overrides[get_user] = get_user_override
    else:
        del app.dependency_overrides[get_user]


@pytest.mark.asyncio(loop_scope="session")
async def test_update_user_by_different_user(api_client):
    new_user = utils.create_user()
    response = await api_client.post(Key.ROUTES.ADD_USER, json=new_user.model_dump())
    assert response.status_code == status.HTTP_201_CREATED
    created_user = response.json()

    get_authenticated_user_override = app.dependency_overrides.get(get_authenticated_user)
    get_user_override = app.dependency_overrides.get(get_user)
    app.dependency_overrides[get_authenticated_user] = utils.get_another_fake_user
    app.dependency_overrides[get_user] = utils.get_another_fake_user

    data = UpdateUser(first_name='MyFirstName', password='MySecretPassword')
    updated_response = await api_client.put(Key.ROUTES.UPDATE_USER.format(user_id=created_user['id']), json=data.model_dump())
    assert updated_response.status_code == status.HTTP_403_FORBIDDEN

    if get_authenticated_user_override:
        app.dependency_overrides[get_authenticated_user] = get_authenticated_user_override
    else:
        del app.dependency_overrides[get_authenticated_user]

    if get_user_override:
        app.dependency_overrides[get_user] = get_user_override
    else:
        del app.dependency_overrides[get_user]

@pytest.mark.asyncio(loop_scope="session")
async def test_update_user_with_no_signed_in_user(api_client_with_boards, with_no_signed_in_user):
    api_client = api_client_with_boards['api_client']
    data = UpdateUser(first_name='MyFirstName', password='MySecretPassword')
    updated_response = await api_client.put(Key.ROUTES.UPDATE_USER.format(user_id='12345678'), json=data.model_dump())
    assert updated_response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.asyncio(loop_scope="session")
async def test_update_invalid_user(api_client_with_boards):
    api_client = api_client_with_boards['api_client']
    data = UpdateUser(first_name='MyFirstName', password='MySecretPassword')
    updated_response = await api_client.put(Key.ROUTES.UPDATE_USER.format(user_id='12345678'), json=data.model_dump())
    assert updated_response.status_code == status.HTTP_403_FORBIDDEN
