"""
Test the models.__init__
"""

# Builtin imports
from pydantic_core import ValidationError

# PyTest imports
import pytest

# Package imports
from recommend_app.db_client.models import RecommendModelType, User, Card, Board, create_model
from recommend_app.db_client.exceptions import RecommendDBModelTypeError

# Local imports
from .. import utils

def test_create_model_factory_user():
    user = create_model(RecommendModelType.USER, {"email_address":utils.get_random_email_address()})
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
    with pytest.raises(ValidationError):
        create_model(RecommendModelType.USER, {"email_id":utils.get_random_email_address()})

def test_create_model_factory_extra_Arg():
    with pytest.raises(ValidationError):
        create_model(RecommendModelType.USER, {"email_address":utils.get_random_email_address(), "first_name": "John"})
