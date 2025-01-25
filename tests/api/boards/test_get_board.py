"""
Test getting boards
"""

# Project specific imports
import pytest
from fastapi import status

# Local imports
from recommend_app.api import constants as Key

#-----------------------------------------------------------------------------#
# Tests
#-----------------------------------------------------------------------------#

@pytest.mark.asyncio(loop_scope="session")
async def test_get_public_board_without_owner_id(api_client_with_boards, with_no_signed_in_user):
    api_client = api_client_with_boards['api_client']
    board = api_client_with_boards['public_board']
    card = api_client_with_boards['card_in_public_board']

    # Get the board (decode_token is overriden. so no user should be returned)
    # But since this is a public, it could be accessed without a signing in.
    got_response = await api_client.get(Key.ROUTES.GET_BOARD.format(board_id=board['id']))
    got_board = got_response.json()
    assert got_board['board']['id'] == board['id']
    assert card['id'] in [c['id'] for c in got_board['cards']]

@pytest.mark.asyncio(loop_scope="session")
async def test_get_public_board_with_owner_id(api_client_with_boards):
    api_client = api_client_with_boards['api_client']
    board = api_client_with_boards['public_board']
    card = api_client_with_boards['card_in_public_board']

    # Get the board. This time, the public board is accessed by the user who created it.
    got_response = await api_client.get(Key.ROUTES.GET_BOARD.format(board_id=board['id']))
    got_board = got_response.json()
    assert got_board['board']['id'] == board['id']
    assert card['id'] in [c['id'] for c in got_board['cards']]

@pytest.mark.asyncio(loop_scope="session")
async def test_get_private_board_without_owner_id(api_client_with_boards, with_no_signed_in_user):
    api_client = api_client_with_boards['api_client']
    board = api_client_with_boards['private_board']

    # Get the board. Private board is being accessed by a non signed in user.
    # Should not work
    response = await api_client.get(Key.ROUTES.GET_BOARD.format(board_id=board['id']))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.asyncio(loop_scope="session")
async def test_get_private_board_with_owner_id(api_client_with_boards):
    api_client = api_client_with_boards['api_client']
    board = api_client_with_boards['private_board']
    card = api_client_with_boards['card_in_private_board']

    # Get the board: private board being accessed by the owner
    got_response = await api_client.get(Key.ROUTES.GET_BOARD.format(board_id=board['id']))
    got_board = got_response.json()
    assert got_board['board']['id'] == board['id']
    assert got_board['board']['private']
    assert card['id'] in [c['id'] for c in got_board['cards']]

@pytest.mark.asyncio(loop_scope="session")
async def test_get_non_existent_board(api_client):
    # Valid id
    got_response = await api_client.get(Key.ROUTES.GET_BOARD.format(board_id='67499a9c03cab482dce67297'))
    assert got_response.status_code == status.HTTP_404_NOT_FOUND

    # Invalid id
    got_response = await api_client.get(Key.ROUTES.GET_BOARD.format(board_id='1234'))
    assert got_response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.asyncio(loop_scope="session")
async def test_get_private_board_with_another_owner(api_client_with_boards, with_different_user):
    api_client = api_client_with_boards['api_client']
    board = api_client_with_boards['private_board']

    # Get the board: Private board can only be accessed by its owner. 
    # This should fail.
    got_response = await api_client.get(Key.ROUTES.GET_BOARD.format(board_id=board['id']))
    assert got_response.status_code == status.HTTP_403_FORBIDDEN
