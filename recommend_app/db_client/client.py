"""
Module: client

This module provides the `RecommendDbClient` class, which serves as the primary
interface for interacting with the database. It exposes methods to add, get
and remove users, boards and cards.

Classes:
- RecommendDbClient: Interface to perform CRUD operations (i.e) add, get and
                     remove users, boards and cards.

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
            RecommendDBConnectionError
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
            RecommendDBModelCreationError - If the email_address isn't unique.
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
