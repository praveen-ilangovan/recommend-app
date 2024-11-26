"""
Let us test session
"""

# Project specific imports
from fastapi import status

# Local imports
from .. import utils

def test_session_post(api_client):
    new_user = utils.create_user()
    password = new_user.password

    # Create a user
    api_client.post("/users", json=new_user.model_dump())

    # Login
    response = api_client.post("/session",
                               data={"username": new_user.user_name,
                                     "password": password,
                                     "grant_type": "password"},
                               headers={"content-type": "application/x-www-form-urlencoded"})
    assert response.status_code == status.HTTP_200_OK
    assert response.cookies.get("access_token")

def test_session_post_invalid_credentials(api_client):
    new_user = utils.create_user()
    api_client.post("/users", json=new_user.model_dump())

    # Login
    response = api_client.post("/session",
                               data={"username": new_user.user_name,
                                     "password": "bad_password",
                                     "grant_type": "password"},
                               headers={"content-type": "application/x-www-form-urlencoded"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
