"""
Test suite for Card
"""

# Builtin imports
from pydantic_core import ValidationError

# PyTest imports
import pytest

# Package import
from recommend_app.db_client.models.card import Card

CARD_DATA = {
    "url": "https://www.netflix.com/gb/title/81767635",
    "title": "Godzilla minus one",
    "description": "In postwar Japan, a traumatized former fighter \
                            pilot joins the civilian effort to fight off a \
                            massive nuclear-enhanced monster attacking their \
                            shores.",
    "image": "url/to/the/image",
    "board_uid": "1234"
}


@pytest.fixture(scope="module")
def card():
    return Card(**CARD_DATA)


# Check creation of the card
def test_creating_card_with_url_and_title():
    card = Card(url=CARD_DATA["url"], title=CARD_DATA["title"])
    assert isinstance(card, Card)


def test_creating_card_with_all_attributes(card):
    assert isinstance(card, Card)


def test_creating_card_with_only_url():
    with pytest.raises(ValidationError):
        card = Card(url=CARD_DATA["url"])


# Check the values of the card
def test_card_url(card):
    assert card.url == CARD_DATA["url"]


def test_card_title(card):
    assert card.title == CARD_DATA["title"]


def test_card_description(card):
    assert card.description == CARD_DATA["description"]


def test_card_image(card):
    assert card.image == CARD_DATA["image"]

def test_card_board_uid(card):
    assert card.board_uid == CARD_DATA["board_uid"]


# Check its immutability
def test_card_url_immutability(card):
    with pytest.raises(ValidationError):
        card.url = "Let us change the url"


def test_card_title_immutability(card):
    with pytest.raises(ValidationError):
        card.title = "Let us change the url"


# Check its comparison
def test_comparing_two_cards(card):
    card2 = Card(url=CARD_DATA["url"], title="Godzilla", board_uid="1234")
    assert card == card2


def test_comparing_two_cards_with_diff_url(card):
    card2 = Card(url="https://www.imdb.com/title/tt23289160/", title=CARD_DATA["title"])
    assert card != card2
