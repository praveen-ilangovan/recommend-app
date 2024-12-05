"""
Module: card
============

This module defines the `Card` model, which represents a board in the
recommend_app.
"""

# Builtin imports
from typing import Optional

# Project specific imports
from pydantic import BaseModel, ConfigDict

# Local imports
from ..types import RecommendModelType
from .bases import BaseNewRecommendModel, BaseRecommendModel, BaseUpdateRecommendModel

# -----------------------------------------------------------------------------#
# Attributes
# -----------------------------------------------------------------------------#


class BaseCardAttributes(BaseModel):
    """
    Defines a list of attributes used across CRUD operations. These are the
    attributes common to all the Recommend Card models.

    Args:
        title (str): Title of the card.
        description (str): A short description of what the card is about.
        thumbnail (str): For now, a url. But think about storing them in a bucket.
    """

    title: Optional[str] = None
    description: Optional[str] = None
    thumbnail: Optional[str] = None


class ExtendedCardAttributes(BaseCardAttributes):
    """
    As the name indicates, this has more attributes used in specific models.

    Args:
        url (str): The URL to recommend
    """

    url: str


class FullCardAttributes(ExtendedCardAttributes):
    """
    As the name indicates, this has more attributes used in specific models.

    Args:
        board_id (str): The id of the board the card belongs to.
    """

    board_id: str


# -----------------------------------------------------------------------------#
# Models
# -----------------------------------------------------------------------------#


class NewCard(ExtendedCardAttributes, BaseNewRecommendModel):
    """
    Model to create a new card.

    Args:
        url (str): The URL to recommend
        title (str): Title of the card.
        description (str): A short description of what the card is about.
        thumbnail (str): For now, a url. But think about storing them in a bucket.
    """

    model_config = ConfigDict(
        extra="allow",
        json_schema_extra={
            "example": {
                "url": "https://www.netflix.com/gb/title/81767635",
                "title": "Godzilla",
                "description": "A movie about godzilla in netfilx.",
                "thumbnail": "/link/to/img.jpg",
            }
        },
    )

    # -------------------------------------------------------------------------#
    # Properties
    # -------------------------------------------------------------------------#
    @property
    def model_type(self) -> RecommendModelType:
        """
        Returns the model type

        Returns:
            RecommendModelType: A string representing the type of the model
                (e.g., 'User', 'Board', 'Card').
        """
        return RecommendModelType.CARD


class CardInDb(FullCardAttributes, BaseRecommendModel):
    """
    Model to hold the card data in the db

    Args:
        id (str|int): ID of the board [Unique]
        url (str): The URL to recommend
        title (str): Title of the card.
        description (str): A short description of what the card is about.
        thumbnail (str): For now, a url. But think about storing them in a bucket.
        board_id (str): The id of the board the card belongs to.
    """

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "67407a5d14376db5b4218532",
                "url": "https://www.netflix.com/gb/title/81767635",
                "title": "Godzilla",
                "description": "A movie about godzilla in netfilx.",
                "thumbnail": "/link/to/img.jpg",
                "board_id": "6744a0ddee62a60d03f06d99",
            }
        }
    )

    # -------------------------------------------------------------------------#
    # Properties
    # -------------------------------------------------------------------------#
    @property
    def model_type(self) -> RecommendModelType:
        """
        Returns the model type

        Returns:
            RecommendModelType: A string representing the type of the model
                (e.g., 'User', 'Board', 'Card').
        """
        return RecommendModelType.CARD


class UpdateCard(BaseCardAttributes, BaseUpdateRecommendModel):
    """
    Attributes in the card that can be updated by its owner

    Args:
        title (str): Title of the card.
        description (str): A short description of what the card is about.
        thumbnail (str): For now, a url. But think about storing them in a bucket.
    """

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "",
                "description": "",
                "thumbnail": "",
            }
        }
    )

    # -------------------------------------------------------------------------#
    # Properties
    # -------------------------------------------------------------------------#
    @property
    def model_type(self) -> RecommendModelType:
        """
        Returns the model type

        Returns:
            RecommendModelType: A string representing the type of the model
                (e.g., 'User', 'Board', 'Card').
        """
        return RecommendModelType.CARD
