"""
Test user crud methods
"""

# Project specific imports
import pytest

# Local imports
from recommend_app.db.models.user import NewUser, UserInDb
from recommend_app.db.exceptions import RecommendDBModelCreationError, RecommendDBModelNotFound, RecommendAppDbError
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


@pytest.mark.asyncio(loop_scope="session")
async def test_get_user(db_client, new_user):
    user = await db_client.add_user(new_user)

    # Get the user by his id
    result = await db_client.get_user(id = str(user.id))
    assert result.id == user.id
    assert result.email_address == user.email_address
    assert result.user_name == user.user_name

    # Get the user by email address
    result2 = await db_client.get_user(email_address = user.email_address)
    assert result2.id == user.id
    assert result2.email_address == user.email_address
    assert result2.user_name == user.user_name

    # Get the user by username
    result3 = await db_client.get_user(user_name = user.user_name)
    assert result3.id == user.id
    assert result3.email_address == user.email_address
    assert result3.user_name == user.user_name

@pytest.mark.asyncio(loop_scope="session")
async def test_get_non_existent_user(db_client):
    with pytest.raises(RecommendDBModelNotFound):
        await db_client.get_user(email_address = "fcdsfdsasdvdssdc@gcsdcds.com")
    
    with pytest.raises(RecommendDBModelNotFound):
        await db_client.get_user(id = '67448b3172df3c07f540043b')

@pytest.mark.asyncio(loop_scope="session")
async def test_get_user_no_input(db_client):
    with pytest.raises(RecommendAppDbError):
        await db_client.get_user()
