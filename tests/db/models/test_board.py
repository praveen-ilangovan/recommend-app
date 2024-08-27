"""
Test suite for Board
"""

# Builtin imports
from dataclasses import FrozenInstanceError

# PyTest imports
import pytest

# Package import
from recommend_app.db_client.models.board import Board

###############################################################################
# Fixtures
###############################################################################
@pytest.fixture(scope='module')
def board():
    return Board(name='movies', owner_uid='1234')

# Check creation of the board
def test_creating_board_with_name_and_owner_id():
    board = Board(name="movies", owner_uid="1234")
    assert isinstance(board, Board)

def test_creating_board_with_only_name():
    with pytest.raises(TypeError):
        Board(name="movies")

def test_creating_board_with_only_owner_id():
    with pytest.raises(TypeError):
        Board(owner_uid="movies")

# Check the values of the board
def test_board_name(board):
    assert board.name == "movies"

def test_board_owner_id(board):
    assert board.owner_uid == "1234"

# Check its immutability
def test_board_name_immutability(board):
    with pytest.raises(FrozenInstanceError):
        board.name = "Let us change the name"


def test_board_owner_id_immutability(board):
    with pytest.raises(FrozenInstanceError):
        board.owner_uid = "Let1345"

# Check its comparison
def test_comparing_two_boards(board):
    board2 = Board(name='movies', owner_uid='1234', uid='123456')
    assert board == board2

def test_comparing_two_boards_with_same_name(board):
    board2 = Board(name='movies', owner_uid='123456')
    assert board != board2
