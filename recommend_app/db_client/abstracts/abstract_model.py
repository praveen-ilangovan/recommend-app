"""
Module: abstract_model
======================

This module defines the abstract base class `AbstractRecommendModel`, which
serves as a blueprint for all models in the recommend_app. Models such as User,
Board, and Card will inherit from this class. Each model has a unique
identifier (UID), and subclasses must implement the `type` property to specify
the type of the model.

By using this abstract model, the application ensures that all models share a
consistent structure, making it easier to work with and manage the data across
different types of entities.
"""

# Builtin imports
from abc import ABC, abstractmethod
from pydantic import BaseModel, ConfigDict


class AbstractRecommendModel(BaseModel, ABC):
    """
    Abstract base class for all models in the recommend_app.

    This class provides a common structure for models, including a unique
    identifier (UID). Subclasses must implement the `type` property to specify
    the type of the model, such as User, Board, or Card. The use of `dataclass`
    with `frozen=True` ensures that instances of this class are immutable,
    providing better safety and consistency in the application's data handling.

    Attributes:
        uid (str): A unique identifier for the model instance.
                   This is used to uniquely identify objects within the
                   database.
    """

    # Model is frozen, meaning the attributes cannot be set after
    # initialization. This makes the model hashable. And extra arguments are
    # forbidden.
    model_config = ConfigDict(frozen=True, extra="forbid")

    uid: str = ""

    ###########################################################################
    # Property
    ###########################################################################
    @property
    @abstractmethod
    def type(self) -> str:
        """
        Abstract property that must be implemented by subclasses to define the
        model type.

        Returns:
            str: A string representing the type of the model
                (e.g., 'User', 'Board', 'Card').
        """
