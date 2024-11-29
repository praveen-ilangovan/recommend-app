"""
Test board crud methods
"""

# Project specific imports
import pytest

# Local imports
from recommend_app.db.models.user import UserInDb
from recommend_app.db.models.board import NewBoard, BoardInDb

from .. import utils

#-----------------------------------------------------------------------------#
# Tests
#-----------------------------------------------------------------------------#

@pytest.mark.asyncio(loop_scope="session")
async def test_add_new_board(db_client):
    new_user = utils.create_user()
    user = await db_client.add_user(new_user)

    new_board = NewBoard(name='Movies to watch')
    board = await db_client.add_board(new_board, user)

    assert isinstance(board, BoardInDb)
    assert board.name == new_board.name
    assert board.owner_id == user.id

@pytest.mark.asyncio(loop_scope="session")
async def test_add_new_board_with_non_existent_user(db_client):
    new_user = utils.create_user()
    user = UserInDb(**new_user.model_dump(), id='1234')

    new_board = NewBoard(name='Movies to watch')
    board = await db_client.add_board(new_board, user)

    assert isinstance(board, BoardInDb)
    assert board.name == new_board.name
    assert board.owner_id == user.id

