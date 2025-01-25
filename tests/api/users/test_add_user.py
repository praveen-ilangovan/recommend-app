"""
Test the users endpoint
"""

# Project specific imports
import pytest
from fastapi import status

# Local imports
from recommend_app.api import constants as Key
from ... import utils

#-----------------------------------------------------------------------------#
# Tests
#-----------------------------------------------------------------------------#
@pytest.mark.asyncio(loop_scope="session")
async def test_add_user(api_client):
    new_user = utils.create_user()

    # The trailing slash in the /users/ is important.
    # Without it, the endpoint would get redirected and the response status
    # would be 307
    response = await api_client.post(Key.ROUTES.ADD_USER, json=new_user.model_dump())
    assert response.status_code == status.HTTP_201_CREATED
    
    result = response.json()
    assert result['email_address'] == new_user.email_address

@pytest.mark.asyncio(loop_scope="session")
async def test_duplicate_user(api_client):
    new_user = utils.create_user()

    await api_client.post(Key.ROUTES.ADD_USER, json=new_user.model_dump())
    response = await api_client.post(Key.ROUTES.ADD_USER, json=new_user.model_dump())
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
