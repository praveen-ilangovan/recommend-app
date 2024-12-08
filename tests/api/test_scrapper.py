"""
Test the scrapper endpoint
"""

# Project specific imports
import pytest
from fastapi import status

# Local imports
from recommend_app.api import constants as Key

#-----------------------------------------------------------------------------#
# Tests
#-----------------------------------------------------------------------------#

@pytest.mark.asyncio(loop_scope="session")
async def test_scrapper_an_empty_url(api_client):
    response = await api_client.get(Key.ROUTES.SCRAP.format(url=''))
    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.asyncio(loop_scope="session")
async def test_scrapper_an_invalid_url(api_client):
    response = await api_client.get(Key.ROUTES.SCRAP.format(url='532'))
    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.asyncio(loop_scope="session")
async def test_scrapper_mocked(api_client, mocker):
    func1_mock = mocker.patch("recommend_app.scrapper.using_requests.scrap")
    func1_mock.return_value = {'url': 'https://www.netflix.com/gb/title/1234', 'title':'Godzilla Minus One'}

    response = await api_client.get(Key.ROUTES.SCRAP.format(url='https://www.netflix.com/gb/title/1234'))
    assert response.status_code == status.HTTP_200_OK
    card = response.json()
    assert card['url'] == 'https://www.netflix.com/gb/title/1234'
