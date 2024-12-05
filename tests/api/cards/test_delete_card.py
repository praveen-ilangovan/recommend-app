"""
Right Owner
    Board
        Pub

        Pvt

Wrong Owner
    Board
"""

# Project specific imports
import pytest
from fastapi import status

# Local imports
from recommend_app.db.models.card import UpdateCard
from recommend_app.api import constants as Key

from ... import utils

#-----------------------------------------------------------------------------#
# Tests
#-----------------------------------------------------------------------------#

@pytest.mark.asyncio(loop_scope="session")
async def test_remove_card_in_public_board_right_user(api_client_with_boards):
    api_client = api_client_with_boards['api_client']
    board = api_client_with_boards['public_board']

    response = await api_client.post(Key.ROUTES.ADD_CARD.format(board_id = board['id']), json=utils.create_card().model_dump())
    card = response.json()

    updated_response = await api_client.delete(Key.ROUTES.DELETE_CARD.format(card_id=card['id']))
    assert updated_response.status_code == status.HTTP_204_NO_CONTENT

@pytest.mark.asyncio(loop_scope="session")
async def test_remove_card_in_private_board_right_user(api_client_with_boards):
    api_client = api_client_with_boards['api_client']
    board = api_client_with_boards['private_board']

    response = await api_client.post(Key.ROUTES.ADD_CARD.format(board_id = board['id']), json=utils.create_card().model_dump())
    card = response.json()

    updated_response = await api_client.delete(Key.ROUTES.DELETE_CARD.format(card_id=card['id']))
    assert updated_response.status_code == status.HTTP_204_NO_CONTENT

@pytest.mark.asyncio(loop_scope="session")
async def test_remove_card_in_public_board_diff_user(api_client_with_boards, with_different_user):
    api_client = api_client_with_boards['api_client']
    card = api_client_with_boards['card_in_public_board']

    updated_response = await api_client.delete(Key.ROUTES.DELETE_CARD.format(card_id=card['id']))
    assert updated_response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.asyncio(loop_scope="session")
async def test_remove_card_in_private_board_diff_user(api_client_with_boards, with_different_user):
    api_client = api_client_with_boards['api_client']
    card = api_client_with_boards['card_in_private_board']

    updated_response = await api_client.delete(Key.ROUTES.DELETE_CARD.format(card_id=card['id']))
    assert updated_response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.asyncio(loop_scope="session")
async def test_remove_card_in_public_board_no_user(api_client_with_boards, with_no_signed_in_user):
    api_client = api_client_with_boards['api_client']
    card = api_client_with_boards['card_in_public_board']

    updated_response = await api_client.delete(Key.ROUTES.DELETE_CARD.format(card_id=card['id']))
    assert updated_response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.asyncio(loop_scope="session")
async def test_remove_card_in_private_board_no_user(api_client_with_boards, with_no_signed_in_user):
    api_client = api_client_with_boards['api_client']
    card = api_client_with_boards['card_in_private_board']

    updated_response = await api_client.delete(Key.ROUTES.DELETE_CARD.format(card_id=card['id']))
    assert updated_response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.asyncio(loop_scope="session")
async def test_remove_non_existent_card(api_client_with_boards):
    api_client = api_client_with_boards['api_client']
    updated_response = await api_client.delete(Key.ROUTES.DELETE_CARD.format(card_id='1234'))
    assert updated_response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.asyncio(loop_scope="session")
async def test_remove_non_existent_card_diff_user(api_client_with_boards, with_different_user):
    api_client = api_client_with_boards['api_client']
    updated_response = await api_client.delete(Key.ROUTES.DELETE_CARD.format(card_id='1234'))
    assert updated_response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.asyncio(loop_scope="session")
async def test_remove_non_existent_card_no_user(api_client_with_boards, with_no_signed_in_user):
    api_client = api_client_with_boards['api_client']
    updated_response = await api_client.delete(Key.ROUTES.DELETE_CARD.format(card_id='1234'))
    assert updated_response.status_code == status.HTTP_401_UNAUTHORIZED
