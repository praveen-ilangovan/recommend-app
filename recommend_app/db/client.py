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
from typing import TYPE_CHECKING, Optional, cast

# Local imports
from .exceptions import RecommendDBConnectionError, RecommendAppDbError
from .types import RecommendModelType

if TYPE_CHECKING:
    from .abstracts.abstract_db import AbstractRecommendDB
    from .models.user import NewUser, UserInDb


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

    async def disconnect(self, clear_db: bool = False) -> bool:
        """
        Disconnects the connection
        """
        status = await self.__db.disconnect(clear_db)
        return status

    ###########################################################################
    # Methods: User
    ###########################################################################
    async def add_user(self, new_user: "NewUser") -> "UserInDb":
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
        result = await self.__db.add(new_user)
        return cast("UserInDb", result)

    async def get_user(
        self,
        id: Optional[str] = None,
        email_address: Optional[str] = None,
        user_name: Optional[str] = None,
    ) -> "UserInDb":
        """
        Retrieve a user from the database by their unique attribute: id, email or username.

        Args:
            id (str): The unique identifier of the user.
            email_address (str): Email address of the user.
            user_name (str): User name of the user

        Returns:
            UserInDb: The User object corresponding to the provided UID.

        Raises:
            `RecommendAppDbError`
            `RecommendDBModelNotFound` if the user is not found.
        """
        attrs_dict = {}
        if id is not None:
            attrs_dict["id"] = id
        elif email_address is not None:
            attrs_dict["email_address"] = email_address
        elif user_name is not None:
            attrs_dict["user_name"] = user_name
        else:
            raise RecommendAppDbError(
                "Please provide an id or email or username of the user."
            )

        result = await self.__db.get(RecommendModelType.USER, attrs_dict)
        return cast("UserInDb", result)
