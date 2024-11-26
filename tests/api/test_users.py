"""
Test the users endpoint
"""

# Project specific imports
from fastapi import status

# Local imports
from .. import utils

#-----------------------------------------------------------------------------#
# Tests
#-----------------------------------------------------------------------------#
def test_add_user(api_client):
    new_user = utils.create_user()

    response = api_client.post("/users", json=new_user.model_dump())
    assert response.status_code == status.HTTP_201_CREATED
    
    result = response.json()
    assert result['email_address'] == new_user.email_address
