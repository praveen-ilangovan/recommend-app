"""
Test Boards
"""

# PyTest imports
import pytest

# Package imports
from recommend_app.db_client.models import Board, User, Card
from recommend_app.db_client.exceptions import (RecommendDBModelCreationError,
                                                RecommendDBModelNotFound)

# Local imports
from .. import utils

CARD_DATA = {
    "url": "https://www.netflix.com/gb/title/81767635",
    "title": "Godzilla minus one",
    "description": "In postwar Japan, a traumatized former fighter \
                            pilot joins the civilian effort to fight off a \
                            massive nuclear-enhanced monster attacking their \
                            shores.",
    "image": "url/to/the/image"
}

###############################################################################
# Fixtures
###############################################################################

@pytest.fixture(scope="module")
def user(recommendDBClient):
    return recommendDBClient.add_user(utils.get_random_email_address())

@pytest.fixture(scope="module")
def board(recommendDBClient, user):
    return recommendDBClient.add_board("movies", user)

###############################################################################
# Tests
###############################################################################

def test_add_card(recommendDBClient, board):
    card = recommendDBClient.add_card(**CARD_DATA, board=board)
    assert isinstance(card, Card)

def test_add_card_duplicate(recommendDBClient, user):
    board1 = recommendDBClient.add_board("movies2", user)
    recommendDBClient.add_card(**CARD_DATA, board=board1)
    with pytest.raises(RecommendDBModelCreationError):
        recommendDBClient.add_card(**CARD_DATA, board=board1)

def test_add_card_same_card_diff_board_same_user(recommendDBClient, user):
    board1 = recommendDBClient.add_board("movies3", user)
    board2 = recommendDBClient.add_board("movies4", user)
    recommendDBClient.add_card(**CARD_DATA, board=board1)
    recommendDBClient.add_card(**CARD_DATA, board=board2)

def test_add_card_same_card_same_board_name_two_diff_users(recommendDBClient):
    user1 = recommendDBClient.add_user(utils.get_random_email_address())
    board1 = recommendDBClient.add_board("movies", user1)
    recommendDBClient.add_card(**CARD_DATA, board=board1)

    user2 = recommendDBClient.add_user(utils.get_random_email_address())
    board2 = recommendDBClient.add_board("movies", user2)
    recommendDBClient.add_card(**CARD_DATA, board=board2)

def test_get_card(recommendDBClient):
    user1 = recommendDBClient.add_user(utils.get_random_email_address())
    board1 = recommendDBClient.add_board("movies", user1)
    card1 = recommendDBClient.add_card(**CARD_DATA, board=board1)

    card = recommendDBClient.get_card(card1.uid)

    assert card == card1
    assert card.url == CARD_DATA['url']

def test_get_card_that_doesnt_exist(recommendDBClient):
    with pytest.raises(RecommendDBModelNotFound):
        recommendDBClient.get_card('111111111111111111111111')

def test_get_card_by_url(recommendDBClient):
    user1 = recommendDBClient.add_user(utils.get_random_email_address())
    board1 = recommendDBClient.add_board("movies", user1)
    card1 = recommendDBClient.add_card(**CARD_DATA, board=board1)

    board2 = recommendDBClient.add_board("books", user1)
    card2 = recommendDBClient.add_card(**CARD_DATA, board=board2)

    card3 = recommendDBClient.get_card_by_url(CARD_DATA['url'], board1)
    assert card3 == card1
    assert card3 != card2

    card4 = recommendDBClient.get_card_by_url(CARD_DATA['url'], board2)
    assert card4 == card2
    assert card4 != card1

def test_get_card_by_invalid_url(recommendDBClient, board):
    with pytest.raises(RecommendDBModelNotFound):
        recommendDBClient.get_card_by_url("https://www.netflix.com/gb/title/81767636", board)

def test_get_all_boards(recommendDBClient):
    # setup
    user1 = recommendDBClient.add_user(utils.get_random_email_address())
    board1 = recommendDBClient.add_board("movies", user1)
    
    # card 1
    card1 = recommendDBClient.add_card(**CARD_DATA, board=board1)

    # card 2
    card2 = recommendDBClient.add_card("url", "title", "", "", board=board1)

    # card 3
    card3 = recommendDBClient.add_card("another_url", "title", "", "", board=board1)

    cards = recommendDBClient.get_all_cards(board1)
    assert len(cards) == 3
    assert card1 in cards
    assert card2 in cards
    assert card3 in cards

def test_get_all_cards_from_board_with_no_card(recommendDBClient):
    # setup
    user1 = recommendDBClient.add_user(utils.get_random_email_address())
    board1 = recommendDBClient.add_board("movies", user1)

    with pytest.raises(RecommendDBModelNotFound):
        recommendDBClient.get_all_cards(board1)

def test_get_all_cards_make_sure_from_same_board(recommendDBClient):
    # setup
    user1 = recommendDBClient.add_user(utils.get_random_email_address())
    board1 = recommendDBClient.add_board("movies", user1)
    card1 = recommendDBClient.add_card(**CARD_DATA, board=board1)
    card2 = recommendDBClient.add_card("url", "title", "", "", board=board1)
    board2 = recommendDBClient.add_board("books", user1)
    card3 = recommendDBClient.add_card("another_url", "title", "", "", board=board2)

    cards = recommendDBClient.get_all_cards(board1)
    assert len(cards) == 2
    assert card1 in cards
    assert card2 in cards
    assert card3 not in cards

def test_remove_card(recommendDBClient):
    user1 = recommendDBClient.add_user(utils.get_random_email_address())
    board1 = recommendDBClient.add_board("movies", user1)
    card1 = recommendDBClient.add_card(**CARD_DATA, board=board1)
    card2 = recommendDBClient.add_card("url", "title", "", "", board=board1)
    assert recommendDBClient.remove_card(card1)
    assert len(recommendDBClient.get_all_cards(board1)) == 1

def test_remove_card_non_existent_card(recommendDBClient):
    card = Card(**CARD_DATA)
    with pytest.raises(RecommendDBModelNotFound):
        recommendDBClient.remove_card(card)
