"""
Module: abstract_db

This module provides the `AbstractRecommendDB` class that `RecommendDbClient`
expects as its input.

Classes:
- AbstractRecommendDB: Provides all the methods the client expects to add, get
                       and remove user, board and card models. This helps in
                       keeping the application agnostic of the database
                       framework we end up using.
"""

# Builtin imports
from abc import ABC, abstractmethod
from typing import Optional

# Local imports
from .models.user import User


class AbstractRecommendDB(ABC):
    """Abstract class that defines the interface for database operations.
    Any database implementation class must inherit from this abstract class
    and provide concrete implementations for all the methods outlined here
    to be compatible with the application.

    This ensures a consistent API for database interactions across different
    database backends or implementations.
    """

    def __init__(self):
        super().__init__()

    ###########################################################################
    # Methods: Abstracts
    ###########################################################################
    @abstractmethod
    def connect(self) -> bool:
        """
        Establishes connection to the database.

        Returns:
            True if the connection is successful.
        """

    @abstractmethod
    def add_user(self, email_address: str) -> Optional[User]:
        """
        Add a new user to the db using their email_address. This email address
        has to be unique.

        Args:
            email_address (str) : Email address of the user

        Returns:
            User or None
        """

    @abstractmethod
    def get_user(self, uid: str) -> Optional[User]:
        """
        Get the user from the database using their uniqueID.

        Args:
            uid (str) : User's unique ID

        Returns:
            User
        """

    @abstractmethod
    def get_user_by_email_address(self, email_address: str) -> Optional[User]:
        """
        Get the user from the database using their email address.

        Args:
            email_address (str) : User's email address

        Returns:
            User
        """

    @abstractmethod
    def remove_user(self, user: User) -> bool:
        """
        Remove the user from the database

        Args:
            user (User) : User to be removed

        Returns:
            True if user is removed
        """
