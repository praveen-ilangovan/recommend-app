"""
Test the health endpoint
"""

# Project specific imports
import pytest

# Project specific imports
from fastapi import status

#-----------------------------------------------------------------------------#
# Tests
#-----------------------------------------------------------------------------#
@pytest.mark.asyncio(loop_scope="session")
async def test_show_health(api_client):
    response = await api_client.get("/health")
    assert response.status_code == status.HTTP_200_OK
