"""
Test creating boards
"""

# Project specific imports
import pytest
from fastapi import status

# Local imports
from recommend_app.api.auth import AuthenticatedUser, get_authenticated_user
from recommend_app.api.app import app
from recommend_app.api import constants as Key
from recommend_app.db.models.board import NewBoard

from .. import utils

def get_fake_user():
    new_user = utils.create_user()
    return AuthenticatedUser(sub=new_user.email_address,
                             email_address=new_user.email_address,
                             id='1234',
                             user_name=new_user.user_name,
                             first_name=new_user.first_name,
                             last_name=new_user.last_name)

#----------------------------------------------------------------------------#
# Tests
#----------------------------------------------------------------------------#
@pytest.mark.asyncio(loop_scope="session")
async def test_add_board(api_client):
    app.dependency_overrides[get_authenticated_user] = get_fake_user
    board = NewBoard(name="Test board")

    response = await api_client.post(Key.ROUTES.ADD_BOARD, json=board.model_dump())
    assert response.status_code == status.HTTP_201_CREATED

