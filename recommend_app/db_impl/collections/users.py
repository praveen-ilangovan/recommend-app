"""
Module: users
=============

This module defines the `Users` class, which manages the MongoDB collection
for user data.

The `Users` class inherits from `AbstractCollection` and handles operations
such as adding, finding, and removing user documents in the MongoDB collection.
It also ensures that email addresses are unique by creating a unique index
on the email field.
"""

# Builtin imports
from typing import TYPE_CHECKING

# Local imports
from ..abstract_collection import AbstractCollection
from ...db_client.models import RecommendModelType
from ...db_client.models import constants as ModelKey

if TYPE_CHECKING:
    from pymongo.database import Database as MongoDB


class Users(AbstractCollection):
    """
    Collection class for managing user data in MongoDB.

    The `Users` class provides methods for interacting with the users collection
    in MongoDB. It inherits the basic operations from `AbstractCollection` and
    sets up the collection with a unique index on the email field.

    Attributes:
        model_type (RecommendModelType): Specifies the `RecommendModelType.USER`
        as the model type for this collection.
    """

    def __init__(self, db: "MongoDB"):
        """
        Initializes the `Users` collection with the given MongoDB database
        instance.

        The constructor also creates a unique index on the email field to
        ensure that no duplicate email addresses can be inserted into the
        collection.

        Args:
            db (pymongo.database.Database): The MongoDB database instance.
        """
        super().__init__(db)

        # Make email address a unique key
        self.create_index([ModelKey.RECOMMEND_MODEL_ATTR_EMAIL], unique=True)

    ###########################################################################
    # Properties
    ###########################################################################
    @property
    def model_type(self) -> RecommendModelType:
        """
        Specifies the model type as `RecommendModelType.USER`.

        Returns:
            `RecommendModelType`: The `RecommendModelType.USER` model type.
        """
        return RecommendModelType.USER
