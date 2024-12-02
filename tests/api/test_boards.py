"""
Test creating boards
"""

# Project specific imports
import pytest
from fastapi import status

# Local imports
from recommend_app.api.auth import AuthenticatedUser, get_user, get_authenticated_user, _decode_token
from recommend_app.api.app import app
from recommend_app.api import constants as Key
from recommend_app.db.models.board import NewBoard, UpdateBoard

from .. import utils

def get_fake_user():
    new_user = utils.create_user()
    return AuthenticatedUser(sub=new_user.email_address,
                             email_address=new_user.email_address,
                             id='1234',
                             user_name=new_user.user_name,
                             first_name=new_user.first_name,
                             last_name=new_user.last_name)

def get_another_fake_user():
    new_user = utils.create_user()
    return AuthenticatedUser(sub=new_user.email_address,
                             email_address=new_user.email_address,
                             id='2345',
                             user_name=new_user.user_name,
                             first_name=new_user.first_name,
                             last_name=new_user.last_name)

def get_no_user():
    return None

def override_decode_token():
    return None

#----------------------------------------------------------------------------#
# Tests
#----------------------------------------------------------------------------#
@pytest.mark.asyncio(loop_scope="session")
async def test_add_board(api_client):
    app.dependency_overrides[get_authenticated_user] = get_fake_user
    board = NewBoard(name="Test board")

    response = await api_client.post(Key.ROUTES.ADD_BOARD, json=board.model_dump())

    del app.dependency_overrides[get_authenticated_user]
    assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.asyncio(loop_scope="session")
async def test_add_board_with_no_user(api_client):
    app.dependency_overrides[get_authenticated_user] = get_no_user
    board = NewBoard(name="Test board")

    response = await api_client.post(Key.ROUTES.ADD_BOARD, json=board.model_dump())

    del app.dependency_overrides[get_authenticated_user]
    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.asyncio(loop_scope="session")
async def test_add_board_with_no_user_token_overriden(api_client):
    app.dependency_overrides[_decode_token] = override_decode_token

    board = NewBoard(name="Test board")

    response = await api_client.post(Key.ROUTES.ADD_BOARD, json=board.model_dump())

    del app.dependency_overrides[_decode_token]
    assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT

#-----------------------------------------------------------------------------#
# Get board by its id
#-----------------------------------------------------------------------------#
@pytest.mark.asyncio(loop_scope="session")
async def test_get_public_board_without_owner_id(api_client):

    # Add a public board
    app.dependency_overrides[get_authenticated_user] = get_fake_user
    board = NewBoard(name="Test board")
    response = await api_client.post(Key.ROUTES.ADD_BOARD, json=board.model_dump())
    created_board = response.json()

    # Make sure the decode token returns none
    app.dependency_overrides[_decode_token] = override_decode_token

    # Get the board
    got_response = await api_client.get(Key.ROUTES.GET_BOARD.format(board_id=created_board['id']))
    got_board = got_response.json()

    # Delete the overrides
    del app.dependency_overrides[_decode_token]
    del app.dependency_overrides[get_authenticated_user]

    assert got_board['id'] == created_board['id']

@pytest.mark.asyncio(loop_scope="session")
async def test_get_public_board_with_owner_id(api_client):

    # Add a public board
    app.dependency_overrides[get_authenticated_user] = get_fake_user
    board = NewBoard(name="Test board")
    response = await api_client.post(Key.ROUTES.ADD_BOARD, json=board.model_dump())
    created_board = response.json()

    # Get the board
    app.dependency_overrides[get_user] = get_fake_user
    got_response = await api_client.get(Key.ROUTES.GET_BOARD.format(board_id=created_board['id']))
    got_board = got_response.json()

    # Delete the overrides
    del app.dependency_overrides[get_user]
    del app.dependency_overrides[get_authenticated_user]

    assert got_board['id'] == created_board['id']

@pytest.mark.asyncio(loop_scope="session")
async def test_get_private_board_without_owner_id(api_client):

    # Add a public board
    app.dependency_overrides[get_authenticated_user] = get_fake_user
    board = NewBoard(name="Test board", private=True)
    response = await api_client.post(Key.ROUTES.ADD_BOARD, json=board.model_dump())
    created_board = response.json()

    # Make sure the decode token returns none
    app.dependency_overrides[_decode_token] = override_decode_token

    # Get the board
    got_response = await api_client.get(Key.ROUTES.GET_BOARD.format(board_id=created_board['id']))

    # Delete the overrides
    del app.dependency_overrides[_decode_token]
    del app.dependency_overrides[get_authenticated_user]

    assert got_response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.asyncio(loop_scope="session")
async def test_get_private_board_with_owner_id(api_client):

    # Add a public board
    app.dependency_overrides[get_authenticated_user] = get_fake_user
    board = NewBoard(name="Test board", private=True)
    response = await api_client.post(Key.ROUTES.ADD_BOARD, json=board.model_dump())
    created_board = response.json()

    # Get the board
    app.dependency_overrides[get_user] = get_fake_user
    got_response = await api_client.get(Key.ROUTES.GET_BOARD.format(board_id=created_board['id']))
    got_board = got_response.json()

    # Delete the overrides
    del app.dependency_overrides[get_user]
    del app.dependency_overrides[get_authenticated_user]

    assert got_board['id'] == created_board['id']
    assert got_board['private']

@pytest.mark.asyncio(loop_scope="session")
async def test_get_non_existent_board(api_client):
    # Valid id
    got_response = await api_client.get(Key.ROUTES.GET_BOARD.format(board_id='67499a9c03cab482dce67297'))
    assert got_response.status_code == status.HTTP_404_NOT_FOUND

    # Invalid id
    got_response = await api_client.get(Key.ROUTES.GET_BOARD.format(board_id='1234'))
    assert got_response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.asyncio(loop_scope="session")
async def test_get_private_board_with_another_owner(api_client):

    # Add a public board
    app.dependency_overrides[get_authenticated_user] = get_fake_user
    board = NewBoard(name="Test board", private=True)
    response = await api_client.post(Key.ROUTES.ADD_BOARD, json=board.model_dump())
    created_board = response.json()

    # Get the board
    app.dependency_overrides[get_user] = get_another_fake_user
    got_response = await api_client.get(Key.ROUTES.GET_BOARD.format(board_id=created_board['id']))

    # Delete the overrides
    del app.dependency_overrides[get_user]
    del app.dependency_overrides[get_authenticated_user]

    assert got_response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.asyncio(loop_scope="session")
async def test_update_public_board_right_user(api_client):

    app.dependency_overrides[get_authenticated_user] = get_fake_user
    app.dependency_overrides[get_user] = get_fake_user

    # Add a public board
    board = NewBoard(name="Test board")
    response = await api_client.post(Key.ROUTES.ADD_BOARD, json=board.model_dump())
    created_board = response.json()

    # Make it a private board
    data = UpdateBoard(private=True)
    response = await api_client.put(Key.ROUTES.UPDATE_BOARD.format(board_id=created_board['id']), json=data.model_dump())
    assert response.status_code == status.HTTP_204_NO_CONTENT

    updated_response = await api_client.get(Key.ROUTES.GET_BOARD.format(board_id=created_board['id']))
    updated = updated_response.json()

    # Delete the overrides
    del app.dependency_overrides[get_user]
    del app.dependency_overrides[get_authenticated_user]

    assert updated['private']

@pytest.mark.asyncio(loop_scope="session")
async def test_update_private_board_right_user(api_client):

    app.dependency_overrides[get_authenticated_user] = get_fake_user
    app.dependency_overrides[get_user] = get_fake_user

    # Add a public board
    board = NewBoard(name="Test board", private=True)
    response = await api_client.post(Key.ROUTES.ADD_BOARD, json=board.model_dump())
    created_board = response.json()

    # Make it a public board and also change its name
    data = UpdateBoard(name="Not private anymore", private=False)
    response = await api_client.put(Key.ROUTES.UPDATE_BOARD.format(board_id=created_board['id']), json=data.model_dump())
    assert response.status_code == status.HTTP_204_NO_CONTENT

    updated_response = await api_client.get(Key.ROUTES.GET_BOARD.format(board_id=created_board['id']))
    updated = updated_response.json()

    # Delete the overrides
    del app.dependency_overrides[get_user]
    del app.dependency_overrides[get_authenticated_user]

    assert not updated['private']
    assert updated['name'] == data.name

@pytest.mark.asyncio(loop_scope="session")
async def test_update_public_board_wrong_user(api_client):

    app.dependency_overrides[get_authenticated_user] = get_fake_user
    # Add a public board
    board = NewBoard(name="Test board")
    response = await api_client.post(Key.ROUTES.ADD_BOARD, json=board.model_dump())
    created_board = response.json()

    app.dependency_overrides[get_authenticated_user] = get_another_fake_user
    app.dependency_overrides[get_user] = get_another_fake_user

    # Make it a private board
    data = UpdateBoard(private=True)
    
    result = await api_client.put(Key.ROUTES.UPDATE_BOARD.format(board_id=created_board['id']), json=data.model_dump())
    
    # Delete the overrides
    del app.dependency_overrides[get_user]
    del app.dependency_overrides[get_authenticated_user]
    
    assert result.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.asyncio(loop_scope="session")
async def test_update_private_board_wrong_user(api_client):

    app.dependency_overrides[get_authenticated_user] = get_fake_user
    # Add a public board
    board = NewBoard(name="Test board", private=True)
    response = await api_client.post(Key.ROUTES.ADD_BOARD, json=board.model_dump())
    created_board = response.json()

    app.dependency_overrides[get_authenticated_user] = get_another_fake_user
    app.dependency_overrides[get_user] = get_another_fake_user

    # Make it a private board
    data = UpdateBoard(private=False)
    
    result = await api_client.put(Key.ROUTES.UPDATE_BOARD.format(board_id=created_board['id']), json=data.model_dump())
    
    # Delete the overrides
    del app.dependency_overrides[get_user]
    del app.dependency_overrides[get_authenticated_user]
    
    assert result.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.asyncio(loop_scope="session")
async def test_update_public_board_no_user(api_client):

    app.dependency_overrides[get_authenticated_user] = get_fake_user
    # Add a public board
    board = NewBoard(name="Test board")
    response = await api_client.post(Key.ROUTES.ADD_BOARD, json=board.model_dump())
    created_board = response.json()

    del app.dependency_overrides[get_authenticated_user]
    app.dependency_overrides[_decode_token] = override_decode_token

    # Make it a private board
    data = UpdateBoard(private=True)
    
    result = await api_client.put(Key.ROUTES.UPDATE_BOARD.format(board_id=created_board['id']), json=data.model_dump())
    # Delete the overrides
    del app.dependency_overrides[_decode_token]

    assert result.status_code == status.HTTP_307_TEMPORARY_REDIRECT

@pytest.mark.asyncio(loop_scope="session")
async def test_update_private_board_no_user(api_client):

    app.dependency_overrides[get_authenticated_user] = get_fake_user
    # Add a public board
    board = NewBoard(name="Test board", private=True)
    response = await api_client.post(Key.ROUTES.ADD_BOARD, json=board.model_dump())
    created_board = response.json()

    del app.dependency_overrides[get_authenticated_user]
    app.dependency_overrides[_decode_token] = override_decode_token

    # Make it a private board
    data = UpdateBoard(private=False)
    
    result = await api_client.put(Key.ROUTES.UPDATE_BOARD.format(board_id=created_board['id']), json=data.model_dump())
    # Delete the overrides
    del app.dependency_overrides[_decode_token]

    assert result.status_code == status.HTTP_307_TEMPORARY_REDIRECT


@pytest.mark.asyncio(loop_scope="session")
async def test_update_non_existent_board(api_client):
    app.dependency_overrides[get_authenticated_user] = get_fake_user
    app.dependency_overrides[get_user] = get_fake_user

    # Make it a private board
    data = UpdateBoard(private=False)
    
    response = await api_client.put(Key.ROUTES.UPDATE_BOARD.format(board_id='1234'), json=data.model_dump())

    # Delete the overrides
    del app.dependency_overrides[get_user]
    del app.dependency_overrides[get_authenticated_user]

    assert response.status_code == status.HTTP_404_NOT_FOUND
