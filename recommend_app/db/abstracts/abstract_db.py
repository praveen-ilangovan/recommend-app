"""
Module: db.abstracts.abstract_db
================================

This module defines the abstract base class `AbstractRecommendDB`, which
serves as a blueprint for database interaction within the recommend_app. Any
concrete database implementation must inherit from this class and implement the
required methods for connecting to the database, adding, retrieving, and
removing models such as users, boards, and cards.

This abstraction allows the application to remain database-agnostic and makes
it easier to switch between different database implementations without
modifying the core logic.
"""

# Builtin imports
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..models.bases import BaseNewRecommendModel, BaseRecommendModel
    from ..types import RecommendModelType


class AbstractRecommendDB(ABC):
    """
    Abstract base class for database interactions in the recommend_app.

    This class defines the contract that any concrete database implementation
    must fulfill. It includes methods for connecting to the database, adding
    models, retrieving single or multiple models, and removing models. The
    exact implementation details will vary depending on the specific database
    being used.
    """

    def __init__(self):
        """
        Initialize the AbstractRecommendDB class.

        This constructor is intended to be called by subclasses, ensuring
        proper initialization of the base class.
        """
        super().__init__()

    ###########################################################################
    # Abstracts - Connections
    ###########################################################################
    @abstractmethod
    async def connect(self) -> bool:
        """
        Establish a connection to the database.

        Returns:
            bool: True if the connection was successful, False otherwise.
        """

    @abstractmethod
    async def ping(self) -> bool:
        """
        Check if the connection is still active

        Returns:
            bool: True if the connection was successful, False otherwise.
        """

    @abstractmethod
    async def disconnect(self, clear_db: bool = False) -> bool:
        """
        Removes the connection to the database.
        """

    ###########################################################################
    # Abstracts - CRUD
    ###########################################################################
    @abstractmethod
    async def add(self, model: "BaseNewRecommendModel") -> "BaseRecommendModel":
        """
        Add a new model to the database.

        Args:
            model (BaseNewRecommendModel): Model to be added.

        Returns:
            BaseRecommendModel: The newly created model instance.

        Raises:
            `RecommendDBModelCreationError` - The class that implements this
            method must throw this exception if the model creation failed.
        """

    @abstractmethod
    async def get(
        self, model_type: "RecommendModelType", attrs_dict: dict[str, str]
    ) -> "BaseRecommendModel":
        """
        Retrieve a single model from the database that matches the given
        criteria.

        Args:
            model_type (RecommendModelType): The type of the model to retrieve
                                             (e.g., User, Board, Card).
            attrs_dict (dict[str, Any]): A dictionary of attributes to filter
                                         the model by.

        Returns:
            BaseRecommendModel: The model instance that matches the given criteria.

        Raises:
            `RecommendAppDbError`
            `RecommendDBModelNotFound` - The class that implements this
            method must throw this exception if the model is not found.
        """
