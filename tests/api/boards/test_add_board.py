"""
Test creating new boards
"""

# Project specific imports
import pytest
from fastapi import status

# Local imports
from recommend_app.api import constants as Key

from ... import utils

#----------------------------------------------------------------------------#
# Tests
#----------------------------------------------------------------------------#
@pytest.mark.asyncio(loop_scope="session")
async def test_add_board(api_client, with_authenticated_user):
    board = utils.create_public_board()
    response = await api_client.post(Key.ROUTES.ADD_BOARD, json=board.model_dump())
    assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.asyncio(loop_scope="session")
async def test_add_private_board(api_client, with_authenticated_user):
    board = utils.create_private_board()
    response = await api_client.post(Key.ROUTES.ADD_BOARD, json=board.model_dump())
    assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.asyncio(loop_scope="session")
async def test_add_board_with_no_user(api_client, with_no_signed_in_user):
    board = utils.create_public_board()
    response = await api_client.post(Key.ROUTES.ADD_BOARD, json=board.model_dump())
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
