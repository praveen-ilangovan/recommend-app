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
    board = recommendDBClient.add_board("movies2", user)
    recommendDBClient.add_card(**CARD_DATA, board=board)
    with pytest.raises(RecommendDBModelCreationError):
        recommendDBClient.add_card(**CARD_DATA, board=board)

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
