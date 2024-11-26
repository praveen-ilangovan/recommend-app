"""
Fixtures for api
"""

# Project specific imports
import pytest
from fastapi.testclient import TestClient

# Local imports
from recommend_app.api.app import app, get_db_client

@pytest.fixture()
def TestApp(db_client):
    app.dependency_overrides[get_db_client] = db_client
    return app

@pytest.fixture()
def api_client(TestApp):
    with TestClient(TestApp) as testclient:
        yield testclient

