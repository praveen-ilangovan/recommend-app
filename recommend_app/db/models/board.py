"""
Module: board
============

This module defines the `Board` model, which represents a board in the
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


class BaseBoardAttributes(BaseModel):
    """
    Defines a list of attributes used across CRUD operations. These are the
    attributes common to all the Recommend Board models.

    Args:
        name (str): Name of the board
        private (bool): If true, only the owner can view this board.
    """

    name: str
    private: bool = False


class ExtendedBoardAttributes(BaseBoardAttributes):
    """
    As the name indicates, this has more attributes used in specific models.

    Args:
        owner_id (str|int): Owner ID of the board. The user who creates the board.
    """

    owner_id: str | int


# -----------------------------------------------------------------------------#
# Models
# -----------------------------------------------------------------------------#


class NewBoard(BaseBoardAttributes, BaseNewRecommendModel):
    """
    Model to create a new board.

    Args:
        name (str): Name of the board
        private (bool): If true, only the owner can view this board.
    """

    model_config = ConfigDict(
        extra="allow",
        json_schema_extra={"example": {"name": "Movies to watch", "private": "False"}},
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
        return RecommendModelType.BOARD


class BoardInDb(ExtendedBoardAttributes, BaseRecommendModel):
    """
    Model to hold the board data in the db

    Args:
        id (str|int): ID of the board [Unique]
        name (str): Name of the board
        private (bool): If true, only the owner can view this board.
        owner_id (str|int): Owner ID of the board. The user who creates the board.
    """

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "67407a5d14376db5b4218532",
                "name": "Movies to watch",
                "private": "False",
                "owner_id": "6744a0ddee62a60d03f06d99",
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
        return RecommendModelType.BOARD


class UpdateBoard(BaseUpdateRecommendModel):
    """
    Attributes in the board that can be updated by its owner

    Args:
        name (str): Name of the board
        private (bool): If true, only the owner can view this board.
    """

    name: Optional[str] = None
    private: Optional[bool] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Movies to watch",
                "private": "False",
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
        return RecommendModelType.BOARD
