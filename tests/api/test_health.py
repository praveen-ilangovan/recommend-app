"""
Test the health endpoint
"""

# Project specific imports
from fastapi import status

#-----------------------------------------------------------------------------#
# Tests
#-----------------------------------------------------------------------------#
def test_show_health(api_client):
    response = api_client.get("/health")
    assert response.status_code == status.HTTP_200_OK
