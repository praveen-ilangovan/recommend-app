"""
Package: models

This package contains data models used in the application. These models
represent core entities such as users and cards, and are implemented using
Python's `dataclass` decorator for simplicity and ease of use. The package
provides structured and immutable data types that help to maintain
consistency across the application.

Modules:
- user.py: Defines the `User` class, which represents a user entity, storing
  user-related information such as email address and unique identifier (UID).

- card.py: Defines the `Card` class, an immutable data structure that
  represents a card entity containing details such as URL, title, description,
  image, and unique identifier (UID).

Example usage:
    from recommend_app.db_client.models.user import User
    from recommend_app.db_client.models.card import Card

    user = User(email_address="user@example.com", uid="12345")
    card = Card(url="https://example.com", title="Example Title")

    print(user)  # Output: User[user@example.com]
    print(card)  # Output: Example Title [https://example.com]

This package provides a centralized location for managing the core data models
used throughout the application, ensuring that entities like `User` and `Card`
are consistently represented and easily accessible.
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
    List all the available Models
    """

    USER = Key.RECOMMEND_MODEL_USER
    BOARD = Key.RECOMMEND_MODEL_BOARD
    CARD = Key.RECOMMEND_MODEL_CARD


# Simple factory function to create a model
def create_model(
    model_type: RecommendModelType, attrs_dict: dict[str, Any]
) -> RecommendModel:
    """
    Factory function to create a new instance of the model.

    Args:
      model_type (RecommendModelType): Type of model to be created.
      attrs_dict (dict): Attrs to be passed to the model class.

    Returns:
      User | Board | Card

    Raises:

    """
    if model_type == RecommendModelType.USER:
        return User(**attrs_dict)
    elif model_type == RecommendModelType.BOARD:
        return Board(**attrs_dict)
    elif model_type == RecommendModelType.CARD:
        return Card(**attrs_dict)
    raise RecommendDBModelTypeError(f"Invalid RecommendModelType: {model_type}")
