"""
Test the health endpoint
"""

# Project specific imports
from fastapi.testclient import TestClient
from fastapi import status

# Local imports
from recommend_app.api.app import app

#-----------------------------------------------------------------------------#
# Tests
#-----------------------------------------------------------------------------#
def test_show_health():
    with TestClient(app) as api_client:
        response = api_client.get("/health")
        assert response.status_code == status.HTTP_200_OK
        items = response.json()
        assert items['DB_Client'] == 'active'
