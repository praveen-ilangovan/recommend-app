"""
Test updating boards
"""

# Project specific imports
import pytest
from fastapi import status

# Local imports
from recommend_app.db.models.board import UpdateBoard
from recommend_app.api import constants as Key

from ... import utils

#-----------------------------------------------------------------------------#
# Tests
#-----------------------------------------------------------------------------#

@pytest.mark.asyncio(loop_scope="session")
async def test_update_public_board_right_user(api_client_with_boards):
    api_client = api_client_with_boards['api_client']

    # Add a public board
    board = utils.create_public_board()
    response = await api_client.post(Key.ROUTES.ADD_BOARD, json=board.model_dump())
    created_board = response.json()

    # Make it a private board
    data = UpdateBoard(private=True)
    response = await api_client.put(Key.ROUTES.UPDATE_BOARD.format(board_id=created_board['id']), json=data.model_dump())
    assert response.status_code == status.HTTP_204_NO_CONTENT

    updated_response = await api_client.get(Key.ROUTES.GET_BOARD.format(board_id=created_board['id']))
    updated = updated_response.json()

    assert updated['board']['private']

@pytest.mark.asyncio(loop_scope="session")
async def test_update_private_board_right_user(api_client_with_boards):
    api_client = api_client_with_boards['api_client']

    # Add a private board
    board = utils.create_private_board()
    response = await api_client.post(Key.ROUTES.ADD_BOARD, json=board.model_dump())
    created_board = response.json()

    # Make it a public board and also change its name
    data = UpdateBoard(name="Not private anymore", private=False)
    response = await api_client.put(Key.ROUTES.UPDATE_BOARD.format(board_id=created_board['id']), json=data.model_dump())
    assert response.status_code == status.HTTP_204_NO_CONTENT

    updated_response = await api_client.get(Key.ROUTES.GET_BOARD.format(board_id=created_board['id']))
    updated = updated_response.json()

    assert not updated['board']['private']
    assert updated['board']['name'] == data.name

@pytest.mark.asyncio(loop_scope="session")
async def test_update_public_board_wrong_user(api_client_with_boards, with_different_user):
    api_client = api_client_with_boards['api_client']
    board = api_client_with_boards['public_board']

    # Make it a private board
    # This should fail because only an owner can update the board.
    data = UpdateBoard(private=True)
    result = await api_client.put(Key.ROUTES.UPDATE_BOARD.format(board_id=board['id']), json=data.model_dump())    
    assert result.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.asyncio(loop_scope="session")
async def test_update_private_board_wrong_user(api_client_with_boards, with_different_user):
    api_client = api_client_with_boards['api_client']
    board = api_client_with_boards['private_board']

    # Make it a public board
    # This should fail because only an owner can update the board.
    data = UpdateBoard(private=False)
    result = await api_client.put(Key.ROUTES.UPDATE_BOARD.format(board_id=board['id']), json=data.model_dump())
    assert result.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.asyncio(loop_scope="session")
async def test_update_public_board_no_user(api_client_with_boards, with_no_signed_in_user):
    api_client = api_client_with_boards['api_client']
    board = api_client_with_boards['public_board']

    # Make it a private board
    # This should fail because only an owner can update the board.
    data = UpdateBoard(private=True)
    result = await api_client.put(Key.ROUTES.UPDATE_BOARD.format(board_id=board['id']), json=data.model_dump())
    assert result.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.asyncio(loop_scope="session")
async def test_update_private_board_no_user(api_client_with_boards, with_no_signed_in_user):
    api_client = api_client_with_boards['api_client']
    board = api_client_with_boards['private_board']

    # Make it a private board
    data = UpdateBoard(private=False)
    result = await api_client.put(Key.ROUTES.UPDATE_BOARD.format(board_id=board['id']), json=data.model_dump())
    assert result.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio(loop_scope="session")
async def test_update_non_existent_board(api_client_with_boards):
    api_client = api_client_with_boards['api_client']

    # Make it a private board
    data = UpdateBoard(private=False)
    response = await api_client.put(Key.ROUTES.UPDATE_BOARD.format(board_id='1234'), json=data.model_dump())
    assert response.status_code == status.HTTP_404_NOT_FOUND
