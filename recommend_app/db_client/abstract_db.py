"""
Module: abstract_db

This module defines the `AbstractRecommendDB` class, an abstract base class
(ABC) that outlines the contract for database operations related to this
application. Any concrete database implementation must inherit from this class
and implement the abstract methods for connecting to the database and
performing operations such as adding, retrieving, and removing users, boards
and cards.

Classes:
- AbstractRecommendDB: An abstract base class that serves as a blueprint for
  database implementations. It defines methods that must be implemented by any
  class intending to interact with the application's database.

Example implementation:
    class MySQLRecommendDB(AbstractRecommendDB):
        def connect(self) -> bool:
            # Implementation for MySQL database connection
            pass

        def add_user(self, email_address: str) -> Optional[User]:
            # Implementation for adding a user in MySQL database
            pass

        def get_user(self, uid: str) -> Optional[User]:
            # Implementation for retrieving a user by UID from MySQL
            pass

        def get_user_by_email_address(self, email_address: str) -> Optional[User]:
            # Implementation for retrieving a user by email from MySQL
            pass

        def remove_user(self, user: User) -> bool:
            # Implementation for removing a user from MySQL database
            pass

This module ensures that any database implementation for the recommend_app
follows a consistent interface, making it easier to switch between different
databases without modifying the core application logic.
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
        Establishes a connection to the database.

        Returns:
            Must return `True` on successful connection, otherwise `False`.
        """

    @abstractmethod
    def add_user(self, email_address: str) -> Optional[User]:
        """
        Adds a new user to the database based on the provided email address.
        Must return the created `User` object on success, or `None` if
        creation fails.

        Args:
            email_address (str) : Email address of the user

        Returns:
            User
        """

    @abstractmethod
    def get_user(self, uid: str) -> Optional[User]:
        """
        Retrieves a user from the database by their unique identifier. Must
        return the `User` object if found, or `None` if the user is not found.

        Args:
            uid (str) : User's unique ID

        Returns:
            User
        """

    @abstractmethod
    def get_user_by_email_address(self, email_address: str) -> Optional[User]:
        """
        Retrieves a user from the database by their email address. Must return
        the `User` object if found, or `None` if the user is not found.

        Args:
            email_address (str) : User's email address

        Returns:
            User
        """

    @abstractmethod
    def remove_user(self, user: User) -> bool:
        """
        Removes the specified `User` from the database. Must return `True` if
        the removal is successful, otherwise `False`.

        Args:
            user (User) : User to be removed

        Returns:
            bool
        """
