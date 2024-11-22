"""
Module: db.client
========================

This module defines the `RecommendDbClient` class, which acts as a client for
interacting with the underlying database that stores the data for the
recommend_app. It handles operations related to users, boards, and cards,
including adding, retrieving, and removing entities. The `RecommendDbClient`
class abstracts away the direct interactions with the database, making it
easier to manage and extend the application's data storage layer.
"""

# Builtin imports
from typing import TYPE_CHECKING

# Local imports
from .models.user import NewUser
from .exceptions import RecommendDBConnectionError

if TYPE_CHECKING:
    from .abstracts.abstract_db import AbstractRecommendDB


class RecommendDbClient:
    """
    A client class for managing operations related to users, boards, and cards
    in the recommend_app database.

    This class interacts with an abstract database layer defined by the
    `AbstractRecommendDB` interface. It provides methods to add, retrieve, and
    remove users, boards, and cards. The class also manages the connection to
    the database and handles exceptions related to database connectivity.

    Attributes:
        __db (AbstractRecommendDB): The database instance used for storage and
        retrieval of data.
    """

    def __init__(self, db: "AbstractRecommendDB"):
        """
        Initialize the RecommendDbClient with a specific database
        implementation.

        Args:
            db (AbstractRecommendDB): An instance of a class implementing the
                                      AbstractRecommendDB interface, which
                                      defines the database operations.
        """
        self.__db = db

    ###########################################################################
    # Methods: DB
    ###########################################################################
    async def connect(self) -> bool:
        """
        Establish a connection to the database.

        Returns:
            True if connection is successful.

        Raises:
            RecommendDBConnectionError: If the connection to the database fails.
        """
        status: bool = await self.__db.connect()
        if not status:
            raise RecommendDBConnectionError(
                f"Connection to {self.__db.__class__.__name__} failed."
            )
        return status

    async def ping(self) -> bool:
        """
        Checks the connection

        Returns:
            True if the connection exist
        """
        status = await self.__db.ping()
        return status

    async def disconnect(self) -> bool:
        """
        Disconnects the connection
        """
        status = await self.__db.disconnect()
        return status

    ###########################################################################
    # Methods: User
    ###########################################################################
    async def add_user(self, new_user: NewUser):
        """
        Add a new user to the database.

        Args:
            new_user (NewUser): Data model that has the details of the new user
                including email_address, user_name, first and last_name and password.

        Returns:
            User: The newly created User object.

        Raises:
            `RecommendDBModelCreationError` if user creation fails.
        """
        print(new_user)
