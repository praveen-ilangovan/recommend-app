"""

Signed in User
    Right Board
        Public Board
            Add card - works
            Add same card twice - fails
        Private Board
            Add card - works

        Add same card in two diff boards - works
    
    Wrong Board
        Public Board
            Add card - fail
        Private Board
            Add card - fail
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
async def test_add_card_to_public_board(api_client_with_boards):
    api_client = api_client_with_boards['api_client']
    board = api_client_with_boards['public_board']

    card = utils.create_card()
    response = await api_client.post(Key.ROUTES.ADD_CARD.format(board_id = board['id']), json=card.model_dump())
    assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.asyncio(loop_scope="session")
async def test_add_card_to_private_board(api_client_with_boards):
    api_client = api_client_with_boards['api_client']
    board = api_client_with_boards['private_board']

    card = utils.create_card()
    response = await api_client.post(Key.ROUTES.ADD_CARD.format(board_id = board['id']), json=card.model_dump())
    assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.asyncio(loop_scope="session")
async def test_add_duplicate_cards(api_client_with_boards):
    api_client = api_client_with_boards['api_client']
    board = api_client_with_boards['public_board']

    card = utils.create_card()
    await api_client.post(Key.ROUTES.ADD_CARD.format(board_id = board['id']), json=card.model_dump())
    response = await api_client.post(Key.ROUTES.ADD_CARD.format(board_id = board['id']), json=card.model_dump())
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

@pytest.mark.asyncio(loop_scope="session")
async def test_add_same_cards_two_different_boards(api_client_with_boards):
    api_client = api_client_with_boards['api_client']
    board1 = api_client_with_boards['public_board']
    board2 = api_client_with_boards['private_board']

    card = utils.create_card()
    response1 = await api_client.post(Key.ROUTES.ADD_CARD.format(board_id = board1['id']), json=card.model_dump())
    response2 = await api_client.post(Key.ROUTES.ADD_CARD.format(board_id = board2['id']), json=card.model_dump())
    assert response1.status_code == status.HTTP_201_CREATED
    assert response2.status_code == status.HTTP_201_CREATED

@pytest.mark.asyncio(loop_scope="session")
async def test_add_card_to_board_of_different_user(api_client_with_boards, with_different_user):
    api_client = api_client_with_boards['api_client']
    board = api_client_with_boards['public_board']

    card = utils.create_card()
    response = await api_client.post(Key.ROUTES.ADD_CARD.format(board_id = board['id']), json=card.model_dump())
    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.asyncio(loop_scope="session")
async def test_add_card_to_board_with_no_signed_in_user(api_client_with_boards, with_no_signed_in_user):
    api_client = api_client_with_boards['api_client']
    board = api_client_with_boards['public_board']

    card = utils.create_card()
    response = await api_client.post(Key.ROUTES.ADD_CARD.format(board_id = board['id']), json=card.model_dump())
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.asyncio(loop_scope="session")
async def test_add_card_to_non_existent_board(api_client_with_boards):
    api_client = api_client_with_boards['api_client']

    card = utils.create_card()
    response = await api_client.post(Key.ROUTES.ADD_CARD.format(board_id = '1234'), json=card.model_dump())
    assert response.status_code == status.HTTP_404_NOT_FOUND
