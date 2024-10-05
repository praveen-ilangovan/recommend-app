
# PyTest imports
import pytest

# Project specific imports
from fastapi.testclient import TestClient

# Package imports
from recommend_app.api import main

@pytest.fixture(scope='session')
def testclient():
    return TestClient( main.app )

#----------------------------------------------------------------------------#
# Tests
#----------------------------------------------------------------------------#
def test_main_root(testclient):
    response = testclient.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Recommend APP"}
