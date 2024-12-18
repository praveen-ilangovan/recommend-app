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
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..models.bases import (
        BaseNewRecommendModel,
        BaseRecommendModel,
        BaseUpdateRecommendModel,
    )
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

    @abstractmethod
    async def get_all(
        self, model_type: "RecommendModelType", attrs_dict: dict[str, Any]
    ) -> list["BaseRecommendModel"]:
        """
        Retrieve all models from the database that match the given criteria.

        Args:
            model_type (RecommendModelType): The type of the models to retrieve
                                             (e.g., User, Board, Card).
            attrs_dict (dict[str, str]): A dictionary of attributes to filter
                                         the models by.

        Returns:
            list[BaseRecommendModel]: A list of model instances that match the
                                  given criteria.
        """

    @abstractmethod
    async def update(
        self, obj_id: str, update_model: "BaseUpdateRecommendModel"
    ) -> "BaseRecommendModel":
        """
        Updates the model in the database with the provided data. Only the non
        None data is updated.

        Args:
            obj_id (str): Id of the object to be updated.
            update_model (BaseUpdateRecommendModel): Data to be updated.

        Returns:
            BaseRecommendModel: The model instance that matches the given criteria.

        Raises:
            `RecommendDBModelNotFound` if the board is not found
            `RecommendAppDbError` if there is an issue in updating the model
        """

    @abstractmethod
    async def remove(self, model_type: "RecommendModelType", obj_id: str) -> bool:
        """
        Remove a model from the database.

        Args:
            model_type (RecommendModelType): The type of the model to delete
                                             (e.g., User, Board, Card).
            obj_id (str): Id of the object to be deleted.

        Returns:
            bool: True if the model was successfully removed, False otherwise.
        """
