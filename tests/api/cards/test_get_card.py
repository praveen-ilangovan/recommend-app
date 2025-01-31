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
async def test_get_card_in_public_board_right_user(api_client_with_boards):
    api_client = api_client_with_boards['api_client']
    board = api_client_with_boards['public_board']

    # Add a card
    card = utils.create_card()
    response = await api_client.post(Key.ROUTES.ADD_CARD.format(board_id = board['id']), json=card.model_dump())
    created_card = response.json()

    updated_response = await api_client.get(Key.ROUTES.GET_CARD.format(card_id=created_card['id']))
    updated = updated_response.json()
    assert updated['card']['id'] == created_card['id']

@pytest.mark.asyncio(loop_scope="session")
async def test_get_card_in_private_board_right_user(api_client_with_boards):
    api_client = api_client_with_boards['api_client']
    card = api_client_with_boards['card_in_private_board']

    updated_response = await api_client.get(Key.ROUTES.GET_CARD.format(card_id=card['id']))
    updated = updated_response.json()
    assert updated['card']['id'] == card['id']

@pytest.mark.asyncio(loop_scope="session")
async def test_get_card_in_public_board_different_user(api_client_with_boards, with_different_user):
    api_client = api_client_with_boards['api_client']
    card = api_client_with_boards['card_in_public_board']

    updated_response = await api_client.get(Key.ROUTES.GET_CARD.format(card_id=card['id']))
    updated = updated_response.json()
    assert updated['card']['id'] == card['id']

@pytest.mark.asyncio(loop_scope="session")
async def test_get_card_in_private_board_different_user(api_client_with_boards, with_different_user):
    api_client = api_client_with_boards['api_client']
    card = api_client_with_boards['card_in_private_board']

    updated_response = await api_client.get(Key.ROUTES.GET_CARD.format(card_id=card['id']))
    assert updated_response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.asyncio(loop_scope="session")
async def test_get_card_in_public_board_no_user(api_client_with_boards, with_no_signed_in_user):
    api_client = api_client_with_boards['api_client']
    card = api_client_with_boards['card_in_public_board']

    updated_response = await api_client.get(Key.ROUTES.GET_CARD.format(card_id=card['id']))
    updated = updated_response.json()
    assert updated['card']['id'] == card['id']

@pytest.mark.asyncio(loop_scope="session")
async def test_get_card_in_private_board_no_user(api_client_with_boards, with_no_signed_in_user):
    api_client = api_client_with_boards['api_client']
    card = api_client_with_boards['card_in_private_board']

    updated_response = await api_client.get(Key.ROUTES.GET_CARD.format(card_id=card['id']))
    assert updated_response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio(loop_scope="session")
async def test_get_invalid_card(api_client_with_boards):
    api_client = api_client_with_boards['api_client']
    updated_response = await api_client.get(Key.ROUTES.GET_CARD.format(card_id='1234'))
    assert updated_response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.asyncio(loop_scope="session")
async def test_get_invalid_card_diff_user(api_client_with_boards, with_different_user):
    api_client = api_client_with_boards['api_client']
    updated_response = await api_client.get(Key.ROUTES.GET_CARD.format(card_id='1234'))
    assert updated_response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.asyncio(loop_scope="session")
async def test_get_invalid_card_no_user(api_client_with_boards, with_no_signed_in_user):
    api_client = api_client_with_boards['api_client']
    updated_response = await api_client.get(Key.ROUTES.GET_CARD.format(card_id='1234'))
    assert updated_response.status_code == status.HTTP_404_NOT_FOUND
