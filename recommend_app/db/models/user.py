"""
Module: user
============

This module defines the `User` model, which represents a user in the
recommend_app.

The `User` model is crucial for managing user-related data, such as storing
user information and associating users with boards and recommendations within
the app.
"""

# Project specific imports
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict

# Local imports
from ..types import RecommendModelType
from .bases import BaseNewRecommendModel, BaseRecommendModel, BaseUpdateRecommendModel

# -----------------------------------------------------------------------------#
# Attributes
# -----------------------------------------------------------------------------#


class BaseUserAttributes(BaseModel):
    """
    Defines a list of attributes used across CRUD operations. These are the
    attributes common to all the Recommend User models.

    Args:
        user_name (str): User name. Must be unique. Email or user_name is used to
            identify the user.
        first_name (str): First name of the user
        last_name (str): Last name of the user
    """

    user_name: str
    first_name: str
    last_name: str


class ExtendedUserAttributes(BaseUserAttributes):
    """
    As the name indicates, this has more attributes used in specific models.

    Args:
        email_address (emailstr): Email address of the user. Must be unique
        password (str): Sign in password. Encryption happens in the client class.
    """

    email_address: EmailStr
    password: str


# -----------------------------------------------------------------------------#
# Models
# -----------------------------------------------------------------------------#


class NewUser(ExtendedUserAttributes, BaseNewRecommendModel):
    """
    Model to create a new user

    Args:
        email_address (emailstr): Email address of the user. Must be unique
        user_name (str): User name. Must be unique. Email or user_name is used to
            identify the user.
        first_name (str): First name of the user
        last_name (str): Last name of the user
        password (str): Sign in password. Encryption happens in the client class.
    """

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email_address": "john.doe@email.com",
                "user_name": "john_doe",
                "first_name": "John",
                "last_name": "Doe",
                "password": "johnDoe123",
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
        return RecommendModelType.USER


class UserInDb(ExtendedUserAttributes, BaseRecommendModel):
    """
    Model to hold the user data in the db

    Args:
        email_address (emailstr): Email address of the user. Must be unique
        user_name (str): User name. Must be unique. Email or user_name is used to
            identify the user.
        first_name (str): First name of the user
        last_name (str): Last name of the user
        password (str): Sign in password. Will be encrypted before storing
    """

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "67407a5d14376db5b4218532",
                "email_address": "john.doe@email.com",
                "user_name": "john_doe",
                "first_name": "John",
                "last_name": "Doe",
                "password": "ncvdisvbskv1w2ebeh",
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
        return RecommendModelType.USER


class UpdateUser(BaseUpdateRecommendModel):
    """
    User attributes that can be updated by its owner

    Args:
        name (str): Name of the board
        private (bool): If true, only the owner can view this board.
    """

    user_name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "user_name": "",
                "first_name": "",
                "last_name": "",
                "password": "",
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
        return RecommendModelType.USER
