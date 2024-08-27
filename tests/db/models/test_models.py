"""
Test the models.__init__
"""

# PyTest imports
import pytest

# Package imports
from recommend_app.db_client.models import RecommendModelType, User, Card, Board, create_model
from recommend_app.db_client.exceptions import RecommendDBModelTypeError

def test_create_model_factory_user():
    user = create_model(RecommendModelType.USER, {"email_address":"hello@example.com"})
    assert isinstance(user, User)

def test_create_model_factory_board():
    board = create_model(RecommendModelType.BOARD, {"name":"movies", "owner_uid": "1234"})
    assert isinstance(board, Board)

def test_create_model_factory_card():
    card = create_model(RecommendModelType.CARD, {"url":"hello@example.com", "title": "hi"})
    assert isinstance(card, Card)

def test_create_model_factory_invalid():
    with pytest.raises(RecommendDBModelTypeError):
        create_model("InvalidType", {})

def test_create_model_factory_invalid_arg():
    with pytest.raises(TypeError):
        create_model(RecommendModelType.USER, {"email_id":"hello@example.com"})

def test_create_model_factory_extra_Arg():
    with pytest.raises(TypeError):
        create_model(RecommendModelType.USER, {"email_address":"hello@example.com", "first_name": "John"})
