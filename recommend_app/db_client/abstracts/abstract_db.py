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
from typing import Any

# Local imports
from ..models import RecommendModel, RecommendModelType


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

    @abstractmethod
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

    @abstractmethod
    def get_all(
        self, model_type: RecommendModelType, attrs_dict: dict[str, Any]
    ) -> list[RecommendModel]:
        """
        Get all the entities for the given attrs_dict

        Args:
            model_type (RecommendModelType): Type of model
            attrs_dict (dict): Key-value pairs.

        Returns:
            List[Board]

        Raises:
            `RecommendDBModelNotFound` if the boards are not found.
        """

    @abstractmethod
    def remove(self, model: RecommendModel) -> bool:
        """
        Remove the entity from the database.

        Args:
            model (RecommendModel): Model to be deleted.

        Returns:
            bool
        """
