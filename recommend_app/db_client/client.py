"""
Module: recommend_db_client

This module contains the `RecommendDbClient` class, which provides a
higher-level interface to interact with the recommendation database.
The `RecommendDbClient` class abstracts operations such as connecting to the
database, adding, retrieving, and removing the users, boards and cards.

The class relies on an underlying database implementation that adheres to the
`AbstractRecommendDB` interface. This ensures flexibility and allows the
application to work with different database backends by providing a consistent
API.

Classes:
- RecommendDbClient: A wrapper class that interacts with the underlying database
  and handles common operations such as connecting, adding, retrieving, and
  removing users, boards and cards.

Example usage:
    from recommend_app.db_client.client import RecommendDbClient

    db_client = RecommendDbClient(db=SomeRecommendDB())
    db_client.connect()
    new_user = db_client.add_user("user@example.com")
    fetched_user = db_client.get_user(new_user.id)
    db_client.remove_user(fetched_user)

Exceptions:
- RecommendDBConnectionError: Raised when the database connection fails.
- RecommendDBModelCreationError: Raised when a model (e.g., user) creation fails.
- RecommendDBModelNotFound: Raised when a requested model is not found in the database.

Dependencies:
- AbstractRecommendDB: An abstract base class that the underlying database
  implementation must inherit from.
"""

# Builtin imports
from typing import TYPE_CHECKING

# Local imports
from .exceptions import (
    RecommendDBConnectionError,
    RecommendDBModelCreationError,
    RecommendDBModelNotFound,
)

if TYPE_CHECKING:
    from .abstract_db import AbstractRecommendDB
    from .models.user import User


class RecommendDbClient:
    """
    Provides interface to perform CRUD operations (i.e) add, get and remove
    users, boards and cards.

    Args:
        db (AbstractRecommendDB) : Child class inheriting this abstract class.
    """

    def __init__(self, db: "AbstractRecommendDB"):
        self.__db = db

    ###########################################################################
    # Methods
    ###########################################################################
    def connect(self) -> None:
        """
        Establishes connection to the database

        Raises:
            `RecommendDBConnectionError` if the connection fails.
        """
        status = self.__db.connect()
        if not status:
            raise RecommendDBConnectionError(
                f"Connection to {self.__db.__class__.__name__} failed."
            )

    def add_user(self, email_address: str) -> "User":
        """
        Add a new user to the db using their email_address. This email address
        has to be unique.

        Args:
            email_address (str) : Email address of the user

        Returns:
            User

        Raises:
            `RecommendDBModelCreationError` if user creation fails.
        """
        user = self.__db.add_user(email_address)
        if user is None:
            raise RecommendDBModelCreationError(
                f"Failed to create user: {email_address}"
            )
        return user

    def get_user(self, uid: str) -> "User":
        """
        Get the user from the database using their uniqueID.

        Args:
            uid (str) : User's unique ID

        Returns:
            User

        Raises:
            `RecommendDBModelNotFound` if the user is not found.
        """
        user = self.__db.get_user(uid)
        if user is None:
            raise RecommendDBModelNotFound(f"User not found - uid:{uid}")
        return user

    def get_user_by_email_address(self, email_address: str) -> "User":
        """
        Get the user from the database using their email address.

        Args:
            email_address (str) : User's email address

        Returns:
            User

        Raises:
            `RecommendDBModelNotFound` if the user is not found.
        """
        user = self.__db.get_user_by_email_address(email_address)
        if user is None:
            raise RecommendDBModelNotFound(
                f"User not found - email_address:{email_address}"
            )
        return user

    def remove_user(self, user: "User") -> bool:
        """
        Remove the user from the database

        Args:
            user (User) : User to be removed

        Returns:
            True if user is removed
        """
        return self.__db.remove_user(user)