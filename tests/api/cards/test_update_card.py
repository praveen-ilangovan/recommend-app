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
async def test_update_card_in_public_board_right_user(api_client_with_boards):
    api_client = api_client_with_boards['api_client']
    card = api_client_with_boards['card_in_public_board']

    data = UpdateCard(title="Updated Card Title")
    response = await api_client.put(Key.ROUTES.UPDATE_CARD.format(card_id=card['id']), json=data.model_dump())
    assert response.status_code == status.HTTP_204_NO_CONTENT

    updated_response = await api_client.get(Key.ROUTES.GET_CARD.format(card_id=card['id']))
    updated = updated_response.json()
    assert updated['title'] == data.title

@pytest.mark.asyncio(loop_scope="session")
async def test_update_card_in_private_board_right_user(api_client_with_boards):
    api_client = api_client_with_boards['api_client']
    card = api_client_with_boards['card_in_private_board']

    data = UpdateCard(title="Updated Card Title")
    response = await api_client.put(Key.ROUTES.UPDATE_CARD.format(card_id=card['id']), json=data.model_dump())
    assert response.status_code == status.HTTP_204_NO_CONTENT

    updated_response = await api_client.get(Key.ROUTES.GET_CARD.format(card_id=card['id']))
    updated = updated_response.json()
    assert updated['title'] == data.title

@pytest.mark.asyncio(loop_scope="session")
async def test_update_card_in_public_board_diff_user(api_client_with_boards, with_different_user):
    api_client = api_client_with_boards['api_client']
    card = api_client_with_boards['card_in_public_board']

    data = UpdateCard(title="Updated Card Title")
    response = await api_client.put(Key.ROUTES.UPDATE_CARD.format(card_id=card['id']), json=data.model_dump())
    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.asyncio(loop_scope="session")
async def test_update_card_in_private_board_diff_user(api_client_with_boards, with_different_user):
    api_client = api_client_with_boards['api_client']
    card = api_client_with_boards['card_in_private_board']

    data = UpdateCard(title="Updated Card Title")
    response = await api_client.put(Key.ROUTES.UPDATE_CARD.format(card_id=card['id']), json=data.model_dump())
    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.asyncio(loop_scope="session")
async def test_update_card_in_public_board_no_user(api_client_with_boards, with_no_signed_in_user):
    api_client = api_client_with_boards['api_client']
    card = api_client_with_boards['card_in_public_board']

    data = UpdateCard(title="Updated Card Title")
    response = await api_client.put(Key.ROUTES.UPDATE_CARD.format(card_id=card['id']), json=data.model_dump())
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.asyncio(loop_scope="session")
async def test_update_card_in_private_board_no_user(api_client_with_boards, with_no_signed_in_user):
    api_client = api_client_with_boards['api_client']
    card = api_client_with_boards['card_in_private_board']

    data = UpdateCard(title="Updated Card Title")
    response = await api_client.put(Key.ROUTES.UPDATE_CARD.format(card_id=card['id']), json=data.model_dump())
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.asyncio(loop_scope="session")
async def test_update_non_existent_card(api_client_with_boards):
    api_client = api_client_with_boards['api_client']

    data = UpdateCard(title="Updated Card Title")
    response = await api_client.put(Key.ROUTES.UPDATE_CARD.format(card_id='1234'), json=data.model_dump())
    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.asyncio(loop_scope="session")
async def test_update_non_existent_card_diff_user(api_client_with_boards, with_different_user):
    api_client = api_client_with_boards['api_client']

    data = UpdateCard(title="Updated Card Title")
    response = await api_client.put(Key.ROUTES.UPDATE_CARD.format(card_id='1234'), json=data.model_dump())
    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.asyncio(loop_scope="session")
async def test_update_non_existent_card_no_user(api_client_with_boards, with_no_signed_in_user):
    api_client = api_client_with_boards['api_client']

    data = UpdateCard(title="Updated Card Title")
    response = await api_client.put(Key.ROUTES.UPDATE_CARD.format(card_id='1234'), json=data.model_dump())
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
