"""
module: db
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
from .collections import Collection, Users

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
    def __init__(self, dbname: str):
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
        """Returns the instance of the database"""
        return self.__db

    ###########################################################################
    # Methods
    ###########################################################################
    def connect(self) -> bool:
        """
        Establishes connection to the database.

        Connects to the MongoDB Cluster using the environment variables DB_URL,
        DB_USER_ID and DB_PASSWORD. Upon connecting to the cluster,
        the database is created (if it doesn't already exist. Technically,
        mongo doesn't create a db until a document is added to a collection
        within this db).

        Returns:
            True if the connection is successful.
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
        Adds a new model entity to the database. Takes in the type of the model
        to be added and a dictionary of required attributes for the entity.

        Args:
            model_type (RecommendModelType): Type of model
            attrs_dict (dict): Key-value pairs.

        Returns:
            `RecommendModel` - `User` | `Board` | `Card`

        Raises:
            `RecommendDBModelCreationError` - The class that implements this
            method must throw this exception if the model creation failed.
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
        Get the entity from the database that matches the fields set in the
        attrs_dict.

        Args:
            model_type (RecommendModelType): Type of model
            attrs_dict (dict): Key-value pairs.

        Returns:
            `RecommendModel` - `User` | `Board` | `Card`

        Raises:
            `RecommendDBModelNotFound` - The class that implements this
            method must throw this exception if the model is not found.
        """
        collection = self.__collections.get(model_type)
        if not collection:
            msg = f"No collection found for {model_type}."
            raise RecommendDBModelNotFound(msg)

        return collection.find_one(attrs_dict)

    def remove(self, model: RecommendModel) -> bool:
        """
        Remove the entity from the database

        Args:
            model (RecommendModel - User|Board|Card) : model to be removed

        Returns:
            True if model is removed
        """
        collection = self.__collections.get(RecommendModelType(model.type))
        if not collection:
            msg = f"No collection found for {model.type}."
            raise RecommendDBModelNotFound(msg)

        return collection.remove({ModelsKey.RECOMMEND_MODEL_ATTR_ID: model.uid})

    ###########################################################################
    # Methods: Privates
    ###########################################################################
    def __initialize(self, db: "MongoDB") -> None:
        """
        Initializes the db and collections
        """
        self.__db = db
        self.__collections[RecommendModelType.USER] = Users(self.__db)
