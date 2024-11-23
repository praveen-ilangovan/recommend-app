"""
Test user crud methods
"""

# Project specific imports
import pytest

# Local imports
from recommend_app.db.models.user import NewUser, UserInDb
from recommend_app.db.exceptions import RecommendDBModelCreationError
from recommend_app.db.hashing import Hasher

from .. import utils

@pytest.fixture(scope="session")
def new_user():
    new_user = NewUser(email_address="john.doe@mail.com",
                       user_name="john_doe",
                       first_name="John",
                       last_name="Doe",
                       password="password123")
    return new_user

#-----------------------------------------------------------------------------#
# Tests
#-----------------------------------------------------------------------------#

@pytest.mark.asyncio(loop_scope="session")
async def test_add_new_user(db_client, new_user):
    user = await db_client.add_user(new_user)
    assert isinstance(user, UserInDb)
    assert user.email_address == new_user.email_address
    assert Hasher.verify_password(new_user.password, user.password)

@pytest.mark.asyncio(loop_scope="session")
async def test_add_duplicate_email_address(db_client):
    new_user = utils.create_user()
    await db_client.add_user(new_user)
    with pytest.raises(RecommendDBModelCreationError):
        await db_client.add_user(new_user)

@pytest.mark.asyncio(loop_scope="session")
async def test_add_duplicate_username(db_client):
    new_user = utils.create_user()
    await db_client.add_user(new_user)
    new_user.email_address = f"{utils.get_random_name()}@mail.com"
    with pytest.raises(RecommendDBModelCreationError):
        await db_client.add_user(new_user)
