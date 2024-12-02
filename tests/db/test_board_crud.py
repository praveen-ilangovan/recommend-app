"""
Test board crud methods
"""

# Project specific imports
import pytest

# Local imports
from recommend_app.db.models.board import NewBoard, BoardInDb, UpdateBoard
from recommend_app.db.exceptions import RecommendAppDbError, RecommendDBModelNotFound

from .. import utils

#-----------------------------------------------------------------------------#
# Tests
#-----------------------------------------------------------------------------#

@pytest.mark.asyncio(loop_scope="session")
async def test_add_new_board(db_client):
    new_user = utils.create_user()
    user = await db_client.add_user(new_user)

    new_board = NewBoard(name='Movies to watch')
    board = await db_client.add_board(new_board, user.id)

    assert isinstance(board, BoardInDb)
    assert board.name == new_board.name
    assert board.owner_id == user.id

@pytest.mark.asyncio(loop_scope="session")
async def test_add_new_board_with_non_existent_user(db_client):
    new_board = NewBoard(name='Movies to watch')
    board = await db_client.add_board(new_board, '1234')

    assert isinstance(board, BoardInDb)
    assert board.name == new_board.name
    assert board.owner_id == '1234'

@pytest.mark.asyncio(loop_scope="session")
async def test_get_public_board_with_no_owner_id(db_client):
    name = utils.get_random_name()
    new_board = NewBoard(name=name)
    board = await db_client.add_board(new_board, '1234')

    board1 = await db_client.get_board(board.id)
    assert board.id == board1.id
    assert board.owner_id == board1.owner_id

@pytest.mark.asyncio(loop_scope="session")
async def test_get_public_board_with_owner_id(db_client):
    name = utils.get_random_name()
    new_board = NewBoard(name=name)
    board = await db_client.add_board(new_board, '1234')

    board1 = await db_client.get_board(board.id, '1234')
    assert board.id == board1.id
    assert board.owner_id == board1.owner_id

@pytest.mark.asyncio(loop_scope="session")
async def test_get_private_board_without_owner_id(db_client):
    name = utils.get_random_name()
    new_board = NewBoard(name=name, private=True)
    board = await db_client.add_board(new_board, '1234')

    with pytest.raises(RecommendAppDbError) as exc_info:
        await db_client.get_board(board.id)
        assert str(exc_info.value).endswith('Please provide the owner_id')

@pytest.mark.asyncio(loop_scope="session")
async def test_get_private_board_with_owner_id(db_client):
    name = utils.get_random_name()
    new_board = NewBoard(name=name, private=True)
    board = await db_client.add_board(new_board, '1234')

    board1 = await db_client.get_board(board.id, '1234')
    assert board.id == board1.id
    assert board.owner_id == board1.owner_id

@pytest.mark.asyncio(loop_scope="session")
async def test_get_private_board_with_wrong_owner_id(db_client):
    name = utils.get_random_name()
    new_board = NewBoard(name=name, private=True)
    board = await db_client.add_board(new_board, '1234')

    with pytest.raises(RecommendAppDbError) as exc_info:
        await db_client.get_board(board.id, '123')
        assert str(exc_info.value) == "Owner doesn't have access to this private board."

@pytest.mark.asyncio(loop_scope="session")
async def test_get_non_existent_board(db_client):
    with pytest.raises(RecommendDBModelNotFound) as exc_info:
        await db_client.get_board('123')

@pytest.mark.asyncio(loop_scope="session")
async def test_get_all_boards(db_client):
    new_user = utils.create_user()
    user = await db_client.add_user(new_user)

    for _ in range(5):
        new_board = NewBoard(name='Movies to watch')
        await db_client.add_board(new_board, user.id)

    boards = await db_client.get_all_boards(user.id)
    assert len(boards) == 5

@pytest.mark.asyncio(loop_scope="session")
async def test_get_all_boards_of_non_existent_owner(db_client):
    boards = await db_client.get_all_boards('6744a0ddee62a60d03f06d98')
    assert boards == []

    boards = await db_client.get_all_boards('1234')
    assert boards == []

@pytest.mark.asyncio(loop_scope="session")
async def test_get_all_public_boards(db_client):
    new_user = utils.create_user()
    user = await db_client.add_user(new_user)

    for _ in range(3):
        new_board = NewBoard(name='Movies to watch')
        await db_client.add_board(new_board, user.id)

    for _ in range(2):
        new_board = NewBoard(name='Movies to watch', private=True)
        await db_client.add_board(new_board, user.id)

    boards = await db_client.get_all_boards(user.id)
    assert len(boards) == 5

    boards = await db_client.get_all_boards(user.id, only_public=True)
    assert len(boards) == 3

@pytest.mark.asyncio(loop_scope="session")
async def test_update_board(db_client):
    new_user = utils.create_user()
    user = await db_client.add_user(new_user)

    new_board = NewBoard(name='Movies to watch')
    board = await db_client.add_board(new_board, user.id)
    assert not board.private

    data = UpdateBoard(private=True)
    updated = await db_client.update_board(board.id, data)
    assert updated.private

    data = UpdateBoard(name="Test")
    updated = await db_client.update_board(board.id, data)
    assert updated.name == "Test"

@pytest.mark.asyncio(loop_scope="session")
async def test_update_non_existent_board(db_client):
    with pytest.raises(RecommendDBModelNotFound):
        data = UpdateBoard(private=True)
        await db_client.update_board('1234', data)
