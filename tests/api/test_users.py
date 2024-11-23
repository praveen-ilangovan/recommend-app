"""
Test the users endpoint
"""

# Project specific imports
from fastapi.testclient import TestClient
from fastapi import status, HTTPException
import pytest

# Local imports
from recommend_app.api.app import app

from .. import utils

#-----------------------------------------------------------------------------#
# Tests
#-----------------------------------------------------------------------------#
def test_add_user():
    new_user = utils.create_user()

    with TestClient(app) as api_client:
        response = api_client.post("/users", json=new_user.model_dump())
        assert response.status_code == status.HTTP_201_CREATED
        
        result = response.json()
        assert result['email_address'] == new_user.email_address

