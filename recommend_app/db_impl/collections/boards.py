"""
Collection that holds all the board documents
"""

# Builtin imports
from typing import TYPE_CHECKING

# Local imports
from ..abstract_collection import AbstractCollection
from . import constants as Key
from ...db_client.models import RecommendModelType

if TYPE_CHECKING:
    from pymongo.database import Database as MongoDB


class Boards(AbstractCollection):
    def __init__(self, db: "MongoDB"):
        super().__init__(db)

        # Make a unique compound index using name and owner_uid
        self.create_index([Key.BOARD_NAME, Key.BOARD_OWNER_ID], unique=True)

    ###########################################################################
    # Properties
    ###########################################################################
    @property
    def collection_name(self) -> str:
        """Returs the name of this collection"""
        return Key.COL_BOARDS

    @property
    def model_type(self) -> RecommendModelType:
        """Returns the name of the model type this class handles"""
        return RecommendModelType.BOARD
