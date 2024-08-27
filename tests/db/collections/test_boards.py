"""
1. add_board - name, user
2. add_board - name2, user
3. add_board - name, user2
4. add_board - name, user
"""

# PyTest imports
import pytest

# Package imports
from recommend_app.db_client.models import Board, User
from recommend_app.db_client.exceptions import (RecommendDBModelCreationError,
                                                RecommendDBModelNotFound)

###############################################################################
# Fixtures
###############################################################################

@pytest.fixture(scope="module")
def user(recommendDBClient):
    return recommendDBClient.add_user("testBoardsUser1@example.com")


###############################################################################
# Tests
###############################################################################

def test_add_board(recommendDBClient, user):
    board = recommendDBClient.add_board("movies", user)
    assert isinstance(board, Board)

def test_add_another_board_same_user(recommendDBClient, user):
    board = recommendDBClient.add_board("books", user)
    assert isinstance(board, Board)

def test_add_board_duplicate_names(recommendDBClient, user):
    recommendDBClient.add_board("music", user)
    with pytest.raises(RecommendDBModelCreationError):
        recommendDBClient.add_board("music", user)

def test_same_board_diif_users(recommendDBClient, user):
    user2 = recommendDBClient.add_user("testBoardsUser2@example.com")
    recommendDBClient.add_board("bestOf2024", user)
    recommendDBClient.add_board("bestOf2024", user2)

def test_get_board(recommendDBClient, user):
    board = recommendDBClient.add_board("boardToget", user)
    board1 = recommendDBClient.get_board(board.uid)
    assert board == board1
    assert board.name == board1.name
    assert board.uid == board1.uid
    assert board.owner_uid == board1.owner_uid

def test_get_board_that_doesnt_exist(recommendDBClient):
    with pytest.raises(RecommendDBModelNotFound):
        recommendDBClient.get_board('111111111111111111111111')

def test_get_board_by_email_name(recommendDBClient):
    # setup
    user1 = recommendDBClient.add_user("testBoardsUser3@example.com")
    board1 = recommendDBClient.add_board("movies", user1)
    board2 = recommendDBClient.add_board("books", user1)

    user2 = recommendDBClient.add_user("testBoardsUser4@example.com")
    board3 = recommendDBClient.add_board("movies", user2)
    board4 = recommendDBClient.add_board("books", user2)

    board = recommendDBClient.get_board_by_name("movies", user1)
    assert board == board1

    books = recommendDBClient.get_board_by_name("books", user2)
    assert books == board4

def test_get_board_by_invalid_name(recommendDBClient, user):
    with pytest.raises(RecommendDBModelNotFound):
        recommendDBClient.get_board_by_name("invalidBoardName", user)

def test_get_all_boards(recommendDBClient):
    # setup
    user1 = recommendDBClient.add_user("testBoardsUser5@example.com")
    board1 = recommendDBClient.add_board("movies", user1)
    board2 = recommendDBClient.add_board("books", user1)

    user2 = recommendDBClient.add_user("testBoardsUser6@example.com")
    board3 = recommendDBClient.add_board("movies", user2)
    board4 = recommendDBClient.add_board("books", user2)

    boards = recommendDBClient.get_all_boards(user1)
    assert len(boards) == 2
    assert board1 in boards
    assert board2 in boards
    assert board3 not in boards

def test_get_all_boards_just_one_board(recommendDBClient):
    # setup
    user1 = recommendDBClient.add_user("testBoardsUser7@example.com")
    board1 = recommendDBClient.add_board("movies", user1)

    boards = recommendDBClient.get_all_boards(user1)
    assert len(boards) == 1
    assert board1 in boards

def test_get_all_boards_no_boards(recommendDBClient):
    # setup
    user1 = recommendDBClient.add_user("testBoardsUser8@example.com")

    with pytest.raises(RecommendDBModelNotFound):
        recommendDBClient.get_all_boards(user1)

def test_get_all_boards_invalid_user(recommendDBClient):
    user = User(email_address="hi@hello.com")
    with pytest.raises(RecommendDBModelNotFound):
        recommendDBClient.get_all_boards(user)

def test_remove_board(recommendDBClient):
    user1 = recommendDBClient.add_user("testBoardsUser9@example.com")
    board1 = recommendDBClient.add_board("movies", user1)
    recommendDBClient.add_board("books", user1)
    assert recommendDBClient.remove_board(board1)
    assert len(recommendDBClient.get_all_boards(user1)) == 1

def test_remove_board_non_existent_board(recommendDBClient):
    board = Board(name='t@eple.com', owner_uid='66c9fa30ead0ee3fdef76ad2')
    with pytest.raises(RecommendDBModelNotFound):
        recommendDBClient.remove_board(board)
