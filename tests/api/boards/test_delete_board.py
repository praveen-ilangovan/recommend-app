"""
Test deleting a board
"""

# Project specific imports
import pytest
from fastapi import status

# Local imports
from recommend_app.api import constants as Key

from ... import utils

#-----------------------------------------------------------------------------#
# Tests
#-----------------------------------------------------------------------------#

@pytest.mark.asyncio(loop_scope="session")
async def test_delete_public_board_by_owner(api_client_with_boards):
    api_client = api_client_with_boards['api_client']

    # Add a public board
    board = utils.create_public_board()
    response = await api_client.post(Key.ROUTES.ADD_BOARD, json=board.model_dump())
    created_board = response.json()

    response = await api_client.delete(Key.ROUTES.DELETE_BOARD.format(board_id=created_board['id']))
    assert response.status_code == status.HTTP_204_NO_CONTENT

@pytest.mark.asyncio(loop_scope="session")
async def test_delete_private_board_by_owner(api_client_with_boards):
    api_client = api_client_with_boards['api_client']

    # Add a private board
    board = utils.create_private_board()
    response = await api_client.post(Key.ROUTES.ADD_BOARD, json=board.model_dump())
    created_board = response.json()

    response = await api_client.delete(Key.ROUTES.DELETE_BOARD.format(board_id=created_board['id']))
    assert response.status_code == status.HTTP_204_NO_CONTENT

@pytest.mark.asyncio(loop_scope="session")
async def test_delete_public_board_by_different_owner(api_client_with_boards, with_different_user):
    api_client = api_client_with_boards['api_client']
    board = api_client_with_boards['public_board']
    response = await api_client.delete(Key.ROUTES.DELETE_BOARD.format(board_id=board['id']))
    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.asyncio(loop_scope="session")
async def test_delete_private_board_by_different_owner(api_client_with_boards, with_different_user):
    api_client = api_client_with_boards['api_client']
    board = api_client_with_boards['private_board']
    response = await api_client.delete(Key.ROUTES.DELETE_BOARD.format(board_id=board['id']))
    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.asyncio(loop_scope="session")
async def test_delete_public_board_by_no_owner(api_client_with_boards, with_no_signed_in_user):
    api_client = api_client_with_boards['api_client']
    board = api_client_with_boards['public_board']
    response = await api_client.delete(Key.ROUTES.DELETE_BOARD.format(board_id=board['id']))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.asyncio(loop_scope="session")
async def test_delete_private_board_by_no_owner(api_client_with_boards, with_no_signed_in_user):
    api_client = api_client_with_boards['api_client']
    board = api_client_with_boards['private_board']
    response = await api_client.delete(Key.ROUTES.DELETE_BOARD.format(board_id=board['id']))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.asyncio(loop_scope="session")
async def test_delete_non_existent_board(api_client_with_boards):
    api_client = api_client_with_boards['api_client']
    response = await api_client.delete(Key.ROUTES.DELETE_BOARD.format(board_id='1234'))
    assert response.status_code == status.HTTP_404_NOT_FOUND
