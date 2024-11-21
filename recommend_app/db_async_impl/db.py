"""
Module: db
==========
"""

# Builtin imports
import os
from typing import TYPE_CHECKING, Optional, Any

# Project specific imports
from motor.motor_asyncio import AsyncIOMotorClient

# Local imports
from .collections import Collection, Users
from ..db_client.abstracts.abstract_db import AbstractRecommendDB
from ..db_client.models import RecommendModelType, RecommendModel

from ..db_client.exceptions import (
    RecommendDBModelCreationError,
)

if TYPE_CHECKING:
    from motor.motor_asyncio import AsyncIOMotorDatabase


class AsyncRecommendDB(AbstractRecommendDB):
    """
    An asyncronous recommendDB using MongoDB and Motor client
    """

    def __init__(self, dbname: str):
        """
        Initialize the RecommendDB with MongoDB implementation.

        Args:
            dbname (str): Name of the database to be created/queried.
        """
        super().__init__()
        self.__dbname = dbname

        self.__db: Optional["AsyncIOMotorDatabase"] = None

        # Collections
        self.__collections: dict[RecommendModelType, Collection] = {}

    ###########################################################################
    # Properties
    ###########################################################################
    @property
    def _db(self) -> Optional["AsyncIOMotorDatabase"]:
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

        # Check if custom timeout is set.
        serverSelectionTimeoutMS = os.getenv("DB_SERVERSELECTIONTIMEOUT")
        if serverSelectionTimeoutMS is not None:
            client: AsyncIOMotorClient = AsyncIOMotorClient(
                url, serverSelectionTimeoutMS=int(serverSelectionTimeoutMS)
            )
        else:
            client = AsyncIOMotorClient(url)

        # Do this to make sure the connection is established. This throws
        # an exception if there is no connection.
        client.server_info()
        self.__initialize(client[self.__dbname])

        return True

    async def add(
        self, model_type: RecommendModelType, attrs_dict: dict[str, Any]
    ) -> RecommendModel:
        """ """
        collection = self.__collections.get(model_type)
        if not collection:
            msg = f"No collection found for {model_type}."
            raise RecommendDBModelCreationError(msg)

        result = await collection.add(attrs_dict)

        return result

    def get(
        self, model_type: RecommendModelType, attrs_dict: dict[str, Any]
    ) -> RecommendModel:
        """ """

    def get_all(
        self, model_type: RecommendModelType, attrs_dict: dict[str, Any]
    ) -> list[RecommendModel]:
        """ """

    def remove(self, model: RecommendModel) -> bool:
        """ """

    ###########################################################################
    # Methods: Privates
    ###########################################################################
    def __initialize(self, db) -> None:
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
