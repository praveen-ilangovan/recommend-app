"""
Test board related models
"""

# Local imports
from recommend_app.db.models.board import NewBoard, BoardInDb
from recommend_app.db.types import CrudType, RecommendModelType

#-----------------------------------------------------------------------------#
# Tests
#-----------------------------------------------------------------------------#
def test_new_board_model():
    new_board = NewBoard(name="Movies to watch")
    assert new_board.name == "Movies to watch"
    assert new_board.crud_type == CrudType.CREATE
    assert new_board.model_type == RecommendModelType.BOARD

def test_new_board_private_field():
    new_board = NewBoard(name="Movies to watch", private=True)
    assert new_board.private

def test_new_board_extra_fields():
    new_board = NewBoard(name="Movies to watch", private=True, owner_id="1234")
    assert new_board.private
    assert new_board.owner_id == "1234"
