"""
Test url validation
"""

# Project specific imports
import pytest

# Local imports
from recommend_app.exceptions import RecommendAppError
from recommend_app import scrapper

#-----------------------------------------------------------------------------#
# Tests
#-----------------------------------------------------------------------------#
@pytest.mark.parametrize("url", ['/data/Python.html', 532, u'dkakasdkjdjakdjadjfalskdjfalk'])
def test_urls(url):
    with pytest.raises(RecommendAppError):
        scrapper.from_url(url)

def test_invalid_response():
    url = 'https://www.netflix.com/title/not-found'
    with pytest.raises(RecommendAppError):
        scrapper.from_url(url)
