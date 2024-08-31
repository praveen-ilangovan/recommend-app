"""
Module: boards
==============

This module defines the `Boards` class, which manages the MongoDB collection
for board data.

The `Boards` class inherits from `AbstractCollection` and handles operations
such as adding, finding, and removing board documents in the MongoDB collection.
It also ensures that the combination of board name and owner UID is unique by
creating a compound unique index on these fields.
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
    """
    Collection class for managing board data in MongoDB.

    The `Boards` class provides methods for interacting with the boards
    collection in MongoDB. It inherits the basic operations from
    `AbstractCollection` and sets up the collection with a compound unique
    index on the `name` and `owner_uid` fields.

    Attributes:
        model_type (RecommendModelType): Specifies the `RecommendModelType.BOARD`
        as the model type for this collection.
    """

    def __init__(self, db: "MongoDB"):
        """
        Initializes the `Boards` collection with the given MongoDB database
        instance.

        The constructor also creates a compound unique index on the `name` and
        `owner_uid` fields to ensure that no duplicate board names for the
        same owner can be inserted into the collection.

        Args:
            db (pymongo.database.Database): The MongoDB database instance.
        """
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
        """
        Specifies the model type as `RecommendModelType.BOARD`.

        Returns:
            RecommendModelType: The `RecommendModelType.BOARD` model type.
        """
        return RecommendModelType.BOARD
