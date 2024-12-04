"""
Test card crud
"""

# Project specific imports
import pytest
import pytest_asyncio

# Local imports
from recommend_app.db.models.card import CardInDb
from recommend_app.db.exceptions import RecommendDBModelCreationError
from .. import utils

@pytest_asyncio.fixture(loop_scope="session")
async def db_client_with_user_and_boards(db_client):
    user = await db_client.add_user(utils.create_user())
    pub_board = await db_client.add_board(utils.create_public_board(), user.id)
    pvt_board = await db_client.add_board(utils.create_private_board(), user.id)    

    return {'db_client': db_client,
            'user': user,
            'pub_board': pub_board,
            'pvt_board': pvt_board}

#-----------------------------------------------------------------------------#
# Tests
#-----------------------------------------------------------------------------#

@pytest.mark.asyncio(loop_scope="session")
async def test_add_card_to_public_board(db_client_with_user_and_boards):
    db_client = db_client_with_user_and_boards['db_client']
    board = db_client_with_user_and_boards['pub_board']

    new_card = utils.create_card()
    card = await db_client.add_card(new_card, board.id)
    assert isinstance(card, CardInDb)
    assert card.board_id == board.id

@pytest.mark.asyncio(loop_scope="session")
async def test_add_card_to_private_board(db_client_with_user_and_boards):
    db_client = db_client_with_user_and_boards['db_client']
    board = db_client_with_user_and_boards['pvt_board']

    new_card = utils.create_card()
    card = await db_client.add_card(new_card, board.id)
    assert isinstance(card, CardInDb)
    assert card.board_id == board.id

@pytest.mark.asyncio(loop_scope="session")
async def test_add_duplicate_cards(db_client_with_user_and_boards):
    db_client = db_client_with_user_and_boards['db_client']
    board = db_client_with_user_and_boards['pub_board']

    new_card = utils.create_card()
    await db_client.add_card(new_card, board.id)

    with pytest.raises(RecommendDBModelCreationError):
        await db_client.add_card(new_card, board.id)


@pytest.mark.asyncio(loop_scope="session")
async def test_add_same_card_to_two_boards(db_client_with_user_and_boards):
    db_client = db_client_with_user_and_boards['db_client']
    pub_board = db_client_with_user_and_boards['pub_board']
    pvt_board = db_client_with_user_and_boards['pvt_board']

    new_card = utils.create_card()
    card1 = await db_client.add_card(new_card, pub_board.id)
    card2 = await db_client.add_card(new_card, pvt_board.id)
    assert card1.url == card2.url
    assert card1.id != card2.id
