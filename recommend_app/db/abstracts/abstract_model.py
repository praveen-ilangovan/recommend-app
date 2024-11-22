"""
Module:db.abstracts.abstract_model
==================================

This module defines the abstract base class `AbstractRecommendModel`, which
serves as a blueprint for all models in the recommend_app. Models such as User,
Board, and Card will inherit from this class. Subclasses must implement the
`crud_type` and `model_type` property to specify the type of the model.

By using this abstract model, the application ensures that all models share a
consistent structure, making it easier to work with and manage the data across
different types of entities.
"""

# Builtin imports
from abc import ABC, abstractmethod
from pydantic import BaseModel

# Local imports
from ..types import RecommendModelType, CrudType


class AbstractRecommendModel(BaseModel, ABC):
    """
    Abstract base class for all models in the recommend_app.
    """

    ###########################################################################
    # Abstracts: Properties
    ###########################################################################
    @property
    @abstractmethod
    def crud_type(self) -> CrudType:
        """
        Abstract property that must be implemented by subclasses to define the
        crud type. If the model is used to create an object, then crud_type is
        set to create. Other types are read and update

        Returns:
            CrudType: Crud operation to be performed.
        """

    @property
    @abstractmethod
    def model_type(self) -> RecommendModelType:
        """
        Abstract property that must be implemented by subclasses to define the
        model type.

        Returns:
            RecommendModelType: A string representing the type of the model
                (e.g., 'User', 'Board', 'Card').
        """

    ###########################################################################
    # Property
    ###########################################################################
    @property
    def type(self) -> str:
        """
        Returns the class type.

        Returns:
            str: A string representing the type of the class
        """
        return self.__class__.__name__
