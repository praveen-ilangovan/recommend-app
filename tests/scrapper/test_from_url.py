"""
Test scrapper from_url
"""

# Local imports
from recommend_app import scrapper
from recommend_app.db.models.card import NewCard

#-----------------------------------------------------------------------------#
# Tests
#-----------------------------------------------------------------------------#

def test_from_url_works(mocker):
    func1_mock = mocker.patch("recommend_app.scrapper.using_requests.scrap")
    func1_mock.return_value = {'url': 'https://www.netflix.com/gb/title/1234', 'title':'Godzilla Minus One'}

    card = scrapper.from_url('https://www.netflix.com/gb/title/81767635')
    assert isinstance(card, NewCard)
    assert card.url == 'https://www.netflix.com/gb/title/1234'
    assert card.title == 'Godzilla Minus One'
    assert not card.description
 
def test_from_url_no_returned_url(mocker):
    func1_mock = mocker.patch("recommend_app.scrapper.using_requests.scrap")
    func1_mock.return_value = {}

    card = scrapper.from_url('https://www.netflix.com/gb/title/81767635')
    assert isinstance(card, NewCard)
    assert card.url == 'https://www.netflix.com/gb/title/81767635'
    assert not card.title
    assert not card.description
