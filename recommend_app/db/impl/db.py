"""
Module: db.impl.db
==================

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
- `motor`: Async client for MongoDB
"""

# Builtin imports
import os
from typing import TYPE_CHECKING, Optional

# Project specific imports
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import OperationFailure

# Local imports
from ..abstracts.abstract_db import AbstractRecommendDB
from ..exceptions import RecommendDBConnectionError


if TYPE_CHECKING:
    from motor.motor_asyncio import AsyncIOMotorDatabase


class RecommendDB(AbstractRecommendDB):
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
    async def connect(self) -> bool:
        """
        Establishes a connection to the MongoDB database.

        This method retrieves the MongoDB connection URL and credentials from
        environment variables, attempts to connect to the MongoDB instance, and
        initializes the database collections.

        Returns:
            bool: True if the connection is successful, False otherwise.

        Raises:
            RecommendDBConnectionError: If the connection to the database fails.
        """
        try:
            db_url = os.environ["DB_URL"]
            db_user_id = os.environ["DB_USER_ID"]
            db_pwd = os.environ["DB_PASSWORD"]
        except KeyError as err:
            raise RecommendDBConnectionError("Failed to connect to the DB") from err

        url = db_url.format(USER=db_user_id, PWD=db_pwd)

        # Create a new client and connect to the server
        # Check if custom timeout is set.
        serverSelectionTimeoutMS = os.getenv("DB_SERVERSELECTIONTIMEOUT")
        if serverSelectionTimeoutMS is not None:
            client: AsyncIOMotorClient = AsyncIOMotorClient(
                url, serverSelectionTimeoutMS=int(serverSelectionTimeoutMS)
            )
        else:
            client = AsyncIOMotorClient(url)

        try:
            await client.admin.command("ping")
        except OperationFailure as err:
            raise RecommendDBConnectionError("Failed to connect to the DB") from err

        return True
