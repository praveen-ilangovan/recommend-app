"""
Test board related models
"""

# Local imports
from recommend_app.db.models.card import NewCard
from recommend_app.db.types import CrudType, RecommendModelType

from ... import utils

#-----------------------------------------------------------------------------#
# Tests
#-----------------------------------------------------------------------------#
def test_new_card_model():
    new_card = utils.create_card()
    assert new_card.crud_type == CrudType.CREATE
    assert new_card.model_type == RecommendModelType.CARD

def test_new_card_extra_fields():
    new_card = utils.create_card()
    card = NewCard(**new_card.model_dump(), board_id="1234")
    assert card.board_id == "1234"
