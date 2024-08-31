"""
Module: abstract_db.py
======================

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
from typing import Any

# Local imports
from ..models import RecommendModel, RecommendModelType


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
    # Methods: Abstracts
    ###########################################################################
    @abstractmethod
    def connect(self) -> bool:
        """
        Establish a connection to the database.

        Returns:
            bool: True if the connection was successful, False otherwise.
        """

    @abstractmethod
    def add(
        self, model_type: RecommendModelType, attrs_dict: dict[str, Any]
    ) -> RecommendModel:
        """
        Add a new model to the database.

        Args:
            model_type (RecommendModelType): The type of the model to be added
                                             (e.g., User, Board, Card).
            attrs_dict (dict[str, Any]): A dictionary of attributes to set for
                                         the new model.

        Returns:
            RecommendModel: The newly created model instance.

        Raises:
            `RecommendDBModelCreationError` - The class that implements this
            method must throw this exception if the model creation failed.
        """

    @abstractmethod
    def get(
        self, model_type: RecommendModelType, attrs_dict: dict[str, Any]
    ) -> RecommendModel:
        """
        Retrieve a single model from the database that matches the given
        criteria.

        Args:
            model_type (RecommendModelType): The type of the model to retrieve
                                             (e.g., User, Board, Card).
            attrs_dict (dict[str, Any]): A dictionary of attributes to filter
                                         the model by.

        Returns:
            RecommendModel: The model instance that matches the given criteria.

        Raises:
            `RecommendDBModelNotFound` - The class that implements this
            method must throw this exception if the model is not found.
        """

    @abstractmethod
    def get_all(
        self, model_type: RecommendModelType, attrs_dict: dict[str, Any]
    ) -> list[RecommendModel]:
        """
        Retrieve all models from the database that match the given criteria.

        Args:
            model_type (RecommendModelType): The type of the models to retrieve
                                             (e.g., User, Board, Card).
            attrs_dict (dict[str, Any]): A dictionary of attributes to filter
                                         the models by.

        Returns:
            list[RecommendModel]: A list of model instances that match the
                                  given criteria.

        Raises:
            `RecommendDBModelNotFound` if the boards are not found.
        """

    @abstractmethod
    def remove(self, model: RecommendModel) -> bool:
        """
        Remove a model from the database.

        Args:
            model (RecommendModel): The model instance to be removed.

        Returns:
            bool: True if the model was successfully removed, False otherwise.
        """
