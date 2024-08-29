"""
Collection that holds all the cards documents
"""

# Builtin imports
from typing import TYPE_CHECKING

# Local imports
from ..abstract_collection import AbstractCollection
from . import constants as Key
from ...db_client.models import RecommendModelType

if TYPE_CHECKING:
    from pymongo.database import Database as MongoDB


class Cards(AbstractCollection):
    def __init__(self, db: "MongoDB"):
        super().__init__(db)

        # Make a unique compound index using url and board_uid
        self.create_index([Key.CARD_URL, Key.CARD_BOARD_UID], unique=True)

    ###########################################################################
    # Properties
    ###########################################################################
    @property
    def collection_name(self) -> str:
        """Returs the name of this collection"""
        return Key.COL_CARDS

    @property
    def model_type(self) -> RecommendModelType:
        """Returns the name of the model type this class handles"""
        return RecommendModelType.CARD
