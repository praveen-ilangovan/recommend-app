"""
Collection that holds all the board documents
"""

# Builtin imports
from typing import TYPE_CHECKING

# Local imports
from ..abstract_collection import AbstractCollection
from ...db_client.models import RecommendModelType
from ...db_client.models import constants as ModelKey

if TYPE_CHECKING:
    from pymongo.database import Database as MongoDB


class Boards(AbstractCollection):
    def __init__(self, db: "MongoDB"):
        super().__init__(db)

        # Make a unique compound index using name and owner_uid
        self.create_index(
            [
                ModelKey.RECOMMEND_MODEL_ATTR_BOARD_NAME,
                ModelKey.RECOMMEND_MODEL_ATTR_BOARD_OWNER_UID,
            ],
            unique=True,
        )

    ###########################################################################
    # Properties
    ###########################################################################
    @property
    def model_type(self) -> RecommendModelType:
        """Returns the name of the model type this class handles"""
        return RecommendModelType.BOARD
