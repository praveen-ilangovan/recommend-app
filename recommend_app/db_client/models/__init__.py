"""
Package: models
===============

The `models` package defines the core data models for the recommend_app,
including `User`, `Board`, and `Card`. These models inherit from
`AbstractRecommendModel` and are used to represent and manage key entities in
the application.

Additionally, this package provides utilities for working with these models,
including:

- `RecommendModel` TypeAlias: A type alias representing any of the core models
                              (`User`, `Board`, or `Card`).
- `RecommendModelType` Enum: An enumeration listing the types of models
                             available in the application.
- `create_model` Function: A factory function for creating instances of the
                           models based on the specified model type.

Modules within this package:
----------------------------
- `user.py`: Contains the `User` model.
- `board.py`: Contains the `Board` model.
- `card.py`: Contains the `Card` model.
- `constants.py`: Defines constants used across the models.

Exceptions:
------------
- `RecommendDBModelTypeError`: Raised when an invalid model type is provided
                               to the `create_model` function.

This package is essential for managing and instantiating the application's data
models, ensuring a consistent and flexible approach to handling different types
of data entities.
"""

# Builtin imports
from typing import TypeAlias, Union, Any
from enum import Enum

# Local imports
from .user import User
from .board import Board
from .card import Card
from ..exceptions import RecommendDBModelTypeError
from . import constants as Key

# Custom data type for Recommend Models
RecommendModel: TypeAlias = Union[User, Board, Card]


# Enum for models
class RecommendModelType(Enum):
    """
    Enumeration for different types of models in the recommend_app.

    Attributes:
        USER: Represents the User model.
        BOARD: Represents the Board model.
        CARD: Represents the Card model.
    """

    USER = Key.RECOMMEND_MODEL_USER
    BOARD = Key.RECOMMEND_MODEL_BOARD
    CARD = Key.RECOMMEND_MODEL_CARD


# Simple factory function to create a model
def create_model(
    model_type: RecommendModelType, attrs_dict: dict[str, Any]
) -> RecommendModel:
    """
    Factory function to create a new instance of a model based on the specified
    type.

    Args:
        model_type (RecommendModelType): The type of model to be created.
                                         Must be one of
                                          `RecommendModelType.USER`,
                                          `RecommendModelType.BOARD`, or
                                          `RecommendModelType.CARD`.
        attrs_dict (dict[str, Any]): A dictionary of attributes to be passed
                                     to the model class constructor.

    Returns:
        RecommendModel: An instance of the specified model type
                        (`User`, `Board`, or `Card`).

    Raises:
        RecommendDBModelTypeError: If an invalid model type is provided.
    """
    if model_type == RecommendModelType.USER:
        return User(**attrs_dict)
    elif model_type == RecommendModelType.BOARD:
        return Board(**attrs_dict)
    elif model_type == RecommendModelType.CARD:
        return Card(**attrs_dict)
    raise RecommendDBModelTypeError(f"Invalid RecommendModelType: {model_type}")
