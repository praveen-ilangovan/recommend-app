"""
Module: cards
=============

This module defines the `Cards` class, which manages the MongoDB collection
for card data.

The `Cards` class inherits from `AbstractCollection` and handles operations
such as adding, finding, and removing card documents in the MongoDB collection.
It also ensures that the combination of card URL and board UID is unique by
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


class Cards(AbstractCollection):
    """
    Collection class for managing card data in MongoDB.

    The `Cards` class provides methods for interacting with the cards collection
    in MongoDB. It inherits the basic operations from `AbstractCollection` and
    sets up the collection with a compound unique index on the `url` and
    `board_uid` fields.

    Attributes:
        model_type (RecommendModelType): Specifies the `RecommendModelType.CARD`
        as the model type for this collection.
    """

    def __init__(self, db: "MongoDB"):
        """
        Initializes the `Cards` collection with the given MongoDB database
        instance.

        The constructor also creates a compound unique index on the `url` and
        `board_uid` fields to ensure that no duplicate card URLs within the
        same board can be inserted into the collection.

        Args:
            db (pymongo.database.Database): The MongoDB database instance.
        """
        super().__init__(db)

        # Make a unique compound index using url and board_uid
        self.create_index(
            [
                ModelKey.RECOMMEND_MODEL_ATTR_CARD_URL,
                ModelKey.RECOMMEND_MODEL_ATTR_CARD_BOARD_UID,
            ],
            unique=True,
        )

    ###########################################################################
    # Properties
    ###########################################################################
    @property
    def model_type(self) -> RecommendModelType:
        """
        Specifies the model type as `RecommendModelType.CARD`.

        Returns:
            RecommendModelType: The `RecommendModelType.CARD` model type.
        """
        return RecommendModelType.CARD
