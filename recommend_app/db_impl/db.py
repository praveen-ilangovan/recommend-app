"""
Module: db
==========

Implements the MongoDB database integration for the RecommendApp.

This module defines the `RecommendDB` class, which provides a MongoDB-backed
implementation of the `AbstractRecommendDB` interface. It manages the
connection to the MongoDB instance, interacts with collections, and performs
CRUD operations for the models used in the application.

Environment Variables:
- `DB_URL`: MongoDB connection URI with placeholders for user credentials.
- `DB_USER_ID`: MongoDB username for authentication.
- `DB_PASSWORD`: MongoDB password for authentication.
- `DB_SERVERSELECTIONTIMEOUT`: (Optional) Timeout for MongoDB server selection
                               in milliseconds.

Dependencies:
- `pymongo`: MongoDB driver for Python.
"""

# Builtin imports
import os
from typing import TYPE_CHECKING, Optional, Any

# Project specific imports
from pymongo import MongoClient
from pymongo.errors import (
    InvalidURI,
    OperationFailure,
    ServerSelectionTimeoutError,
    ConfigurationError,
)

# Local imports
from .collections import Collection, Users, Boards, Cards

# from .collections.users import Users
from ..db_client.abstracts.abstract_db import AbstractRecommendDB
from ..db_client.models import RecommendModelType, RecommendModel
from ..db_client.models import constants as ModelsKey

from ..db_client.exceptions import (
    RecommendDBModelCreationError,
    RecommendDBModelNotFound,
)

if TYPE_CHECKING:
    from pymongo.database import Database as MongoDB


class RecommendDB(AbstractRecommendDB):
    """
    MongoDB-backed implementation of the `AbstractRecommendDB` interface.

    The `RecommendDB` class provides methods for connecting to a MongoDB
    instance and performing CRUD operations on the `User`, `Board`, and `Card`
    collections. It initializes MongoDB collections and ensures that all
    operations conform to the models defined in the application.

    Attributes:
        __dbname (str): The name of the MongoDB database to connect to.
        __db (Optional[MongoDB]): The MongoDB database instance.
        __collections (dict[RecommendModelType, Collection]): A mapping of
            model types to MongoDB collections.
    """

    def __init__(self, dbname: str):
        """
        Initialize the RecommendDB with MongoDB implementation.

        Args:
            dbname (str): Name of the database to be created/queried.
        """
        super().__init__()
        self.__dbname = dbname

        # Database
        self.__db: Optional["MongoDB"] = None

        # Collections
        self.__collections: dict[RecommendModelType, Collection] = {}

    ###########################################################################
    # Properties
    ###########################################################################
    @property
    def _db(self) -> Optional["MongoDB"]:
        """
        Returns the instance of MongoDB object.

        Returns:
            MongoDB: Pointer to the PyMongoDB instance.
        """
        return self.__db

    ###########################################################################
    # Methods
    ###########################################################################
    def connect(self) -> bool:
        """
        Establishes a connection to the MongoDB database.

        This method retrieves the MongoDB connection URL and credentials from
        environment variables, attempts to connect to the MongoDB instance, and
        initializes the database collections.

        Returns:
            bool: True if the connection is successful, False otherwise.
        """
        url = os.environ["DB_URL"].format(
            USER=os.getenv("DB_USER_ID"), PWD=os.getenv("DB_PASSWORD")
        )

        try:
            # Check if custom timeout is set.
            serverSelectionTimeoutMS = os.getenv("DB_SERVERSELECTIONTIMEOUT")
            if serverSelectionTimeoutMS is not None:
                client: MongoClient = MongoClient(
                    url, serverSelectionTimeoutMS=int(serverSelectionTimeoutMS)
                )
            else:
                client = MongoClient(url)

            # Do this to make sure the connection is established. This throws
            # an exception if there is no connection.
            client.server_info()
            self.__initialize(client[self.__dbname])

            return True

        except (
            InvalidURI,
            OperationFailure,
            ServerSelectionTimeoutError,
            ConfigurationError,
        ):
            return False

    def add(
        self, model_type: RecommendModelType, attrs_dict: dict[str, Any]
    ) -> RecommendModel:
        """
        Adds a new document to the specified MongoDB collection.

        This method inserts a new document into the appropriate collection
        based on the model type (e.g., `User`, `Board`, `Card`).

        Args:
            model_type (RecommendModelType): The type of model to add.
            attrs_dict (dict[str, Any]): A dictionary of attributes to be added
                                         as a document.

        Returns:
            `RecommendModel`: The created model instance.

        Raises:
            `RecommendDBModelCreationError`: If the corresponding collection is
                not found.
        """
        collection = self.__collections.get(model_type)
        if not collection:
            msg = f"No collection found for {model_type}."
            raise RecommendDBModelCreationError(msg)

        return collection.add(attrs_dict)

    def get(
        self, model_type: RecommendModelType, attrs_dict: dict[str, Any]
    ) -> RecommendModel:
        """
        Retrieves a document from the specified MongoDB collection.

        This method fetches a single document from the appropriate collection
        based on the model type and the provided criteria.

        Args:
            model_type (RecommendModelType): The type of model to retrieve.
            attrs_dict (dict[str, Any]): A dictionary of attributes to match
                the document.

        Returns:
            `RecommendModel`: The retrieved model instance.

        Raises:
            `RecommendDBModelNotFound`: If the corresponding collection or
                document is not found.
        """
        collection = self.__collections.get(model_type)
        if not collection:
            msg = f"No collection found for {model_type}."
            raise RecommendDBModelNotFound(msg)

        return collection.find_one(attrs_dict)

    def get_all(
        self, model_type: RecommendModelType, attrs_dict: dict[str, Any]
    ) -> list[RecommendModel]:
        """
        Retrieves all documents matching criteria from the specified MongoDB
        collection.

        This method fetches multiple documents from the appropriate collection
        based on the model type and the provided criteria.

        Args:
            model_type (RecommendModelType): The type of model to retrieve.
            attrs_dict (dict[str, Any]): A dictionary of attributes to match
                the documents.

        Returns:
            list[RecommendModel]: A list of retrieved model instances.

        Raises:
            `RecommendDBModelNotFound`: If the corresponding collection is not
                found.
        """
        collection = self.__collections.get(model_type)
        if not collection:
            msg = f"No collection found for {model_type}."
            raise RecommendDBModelNotFound(msg)

        return collection.find_all(attrs_dict)

    def remove(self, model: RecommendModel) -> bool:
        """
        Removes a document from the specified MongoDB collection.

        This method deletes a document from the appropriate collection based on
        the model type and the unique identifier.

        Args:
            model (RecommendModel): The model instance to be removed.

        Returns:
            bool: True if the document was successfully removed, False
                otherwise.

        Raises:
            `RecommendDBModelNotFound`: If the corresponding collection or
                document is not found.
        """
        collection = self.__collections.get(RecommendModelType(model.type))
        if not collection:
            msg = f"No collection found for {model.type}."
            raise RecommendDBModelNotFound(msg)

        return collection.remove({ModelsKey.RECOMMEND_MODEL_ATTR_UID: model.uid})

    ###########################################################################
    # Methods: Privates
    ###########################################################################
    def __initialize(self, db: "MongoDB") -> None:
        """
        Initializes MongoDB collections for the `User`, `Board`, and `Card`
        models.

        This private method is called after successfully connecting to the
        MongoDB instance. It sets up the necessary collections for performing
        CRUD operations.

        Args:
            db (MongoDB): The MongoDB database instance.
        """
        self.__db = db
        self.__collections[RecommendModelType.USER] = Users(self.__db)
        self.__collections[RecommendModelType.BOARD] = Boards(self.__db)
        self.__collections[RecommendModelType.CARD] = Cards(self.__db)
