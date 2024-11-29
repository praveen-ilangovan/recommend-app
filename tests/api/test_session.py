"""
Let us test session
"""

# Project specific imports
import pytest
from fastapi import status

# Local imports
from .. import utils

#-----------------------------------------------------------------------------#
# Tests
#-----------------------------------------------------------------------------#
@pytest.mark.asyncio(loop_scope="session")
async def test_session_post(api_client):
    new_user = utils.create_user()
    password = new_user.password

    # Create a user
    await api_client.post("/users/", json=new_user.model_dump())

    # Login
    response = await api_client.post("/session/",
                               data={"username": new_user.user_name,
                                     "password": password,
                                     "grant_type": "password"},
                               headers={"content-type": "application/x-www-form-urlencoded"})
    assert response.status_code == status.HTTP_200_OK
    assert response.cookies.get("access_token")

@pytest.mark.asyncio(loop_scope="session")
async def test_session_post_with_email(api_client):
    new_user = utils.create_user()
    password = new_user.password

    # Create a user
    await api_client.post("/users/", json=new_user.model_dump())

    # Login
    response = await api_client.post("/session/",
                               data={"username": new_user.email_address,
                                     "password": password,
                                     "grant_type": "password"},
                               headers={"content-type": "application/x-www-form-urlencoded"})
    assert response.status_code == status.HTTP_200_OK
    assert response.cookies.get("access_token")

@pytest.mark.asyncio(loop_scope="session")
async def test_session_post_invalid_credentials(api_client):
    new_user = utils.create_user()
    await api_client.post("/users/", json=new_user.model_dump())

    # Login
    response = await api_client.post("/session/",
                               data={"username": new_user.user_name,
                                     "password": "bad_password",
                                     "grant_type": "password"},
                               headers={"content-type": "application/x-www-form-urlencoded"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.asyncio(loop_scope="session")
async def test_session_logout(api_client):
    new_user = utils.create_user()
    password = new_user.password

    # Create a user
    await api_client.post("/users/", json=new_user.model_dump())

    # Login
    await api_client.post("/session/",
                    data={"username": new_user.user_name,
                          "password": password,
                          "grant_type": "password"},
                    headers={"content-type": "application/x-www-form-urlencoded"})
    
    # Logout
    response = await api_client.get("/session/logout")
    assert not response.cookies.get("access_token")
