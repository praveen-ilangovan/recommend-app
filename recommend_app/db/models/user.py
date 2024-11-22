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
from pydantic import EmailStr, ConfigDict

# Local imports
from ..types import RecommendModelType
from .bases import BaseNewRecommendModel, BaseRecommendModel

# -----------------------------------------------------------------------------#
# Models
# -----------------------------------------------------------------------------#


class NewUser(BaseNewRecommendModel):
    """
    Model to create a new user

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
                "email_address": "john.doe@email.com",
                "user_name": "john_doe",
                "first_name": "John",
                "last_name": "Doe",
                "password": "johnDoe123",
            }
        }
    )

    email_address: EmailStr
    user_name: str
    first_name: str
    last_name: str
    password: str

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


class UserInDb(BaseRecommendModel):
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
                "id": "ObjectId('67407a5d14376db5b4218532')",
                "email_address": "john.doe@email.com",
                "user_name": "john_doe",
                "first_name": "John",
                "last_name": "Doe",
                "hashed_password": "ncvdisvbskv1w2ebeh",
            }
        }
    )

    email_address: EmailStr
    user_name: str
    first_name: str
    last_name: str
    password: str

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
