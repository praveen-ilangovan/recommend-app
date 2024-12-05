"""
Test card crud
"""

# Project specific imports
import pytest
import pytest_asyncio

# Local imports
from recommend_app.db.models.card import CardInDb, UpdateCard
from recommend_app.db.exceptions import RecommendDBModelCreationError, RecommendDBModelNotFound
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

@pytest.mark.asyncio(loop_scope="session")
async def test_get_card(db_client_with_user_and_boards):
    db_client = db_client_with_user_and_boards['db_client']
    pub_board = db_client_with_user_and_boards['pub_board']

    new_card = utils.create_card()
    card1 = await db_client.add_card(new_card, pub_board.id)
    card2 = await db_client.get_card(card1.id)
    assert card1.id == card2.id

@pytest.mark.asyncio(loop_scope="session")
async def test_get_non_existent_card(db_client_with_user_and_boards):
    db_client = db_client_with_user_and_boards['db_client']

    with pytest.raises(RecommendDBModelNotFound):
        await db_client.get_card('1234')

@pytest.mark.asyncio(loop_scope="session")
async def test_get_all_cards(db_client_with_user_and_boards):
    db_client = db_client_with_user_and_boards['db_client']

    user = await db_client.add_user(utils.create_user())
    board = await db_client.add_board(utils.create_public_board(), user.id)

    for _ in range(4):
        await db_client.add_card(utils.create_card(), board.id)

    cards = await db_client.get_all_cards(board.id)
    assert len(cards) == 4

@pytest.mark.asyncio(loop_scope="session")
async def test_get_all_cards_from_non_existent_board(db_client_with_user_and_boards):
    db_client = db_client_with_user_and_boards['db_client']
    cards = await db_client.get_all_cards(['1234'])
    assert not cards

@pytest.mark.asyncio(loop_scope="session")
async def test_update_card_in_public_board(db_client_with_user_and_boards):
    db_client = db_client_with_user_and_boards['db_client']
    pub_board = db_client_with_user_and_boards['pub_board']

    new_card = utils.create_card()
    card1 = await db_client.add_card(new_card, pub_board.id)

    update_data = UpdateCard(title='UpdatedTitle')
    card2 = await db_client.update_card(card1.id, update_data)
    assert card2.title == update_data.title

@pytest.mark.asyncio(loop_scope="session")
async def test_update_card_in_private_board(db_client_with_user_and_boards):
    db_client = db_client_with_user_and_boards['db_client']
    pvt_board = db_client_with_user_and_boards['pvt_board']

    new_card = utils.create_card()
    card1 = await db_client.add_card(new_card, pvt_board.id)

    update_data = UpdateCard(title='UpdatedTitle', thumbnail='test thumbnail')
    card2 = await db_client.update_card(card1.id, update_data)
    assert card2.title == update_data.title
    assert card2.thumbnail == update_data.thumbnail
    assert card2.url == card1.url

@pytest.mark.asyncio(loop_scope="session")
async def test_update_invalid_card(db_client_with_user_and_boards):
    db_client = db_client_with_user_and_boards['db_client']

    update_data = UpdateCard(title='UpdatedTitle', thumbnail='test thumbnail')
    with pytest.raises(RecommendDBModelNotFound):
        await db_client.update_card('1234', update_data)

@pytest.mark.asyncio(loop_scope="session")
async def test_remove_card(db_client_with_user_and_boards):
    db_client = db_client_with_user_and_boards['db_client']
    pub_board = db_client_with_user_and_boards['pub_board']

    new_card = utils.create_card()
    card1 = await db_client.add_card(new_card, pub_board.id)
    assert await db_client.remove_card(card1.id)

@pytest.mark.asyncio(loop_scope="session")
async def test_remove_invalid_card(db_client_with_user_and_boards):
    db_client = db_client_with_user_and_boards['db_client']

    with pytest.raises(RecommendDBModelNotFound):
        await db_client.remove_card('1234')
