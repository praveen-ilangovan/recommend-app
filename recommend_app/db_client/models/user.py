"""
Module: user

This module defines the `User` class, which represents a user entity in the
recommend_app. The `User` class is a simple data structure implemented using
Python's `dataclass` decorator, which provides an easy way to create classes
that primarily store data.

Classes:
- User: Represents a user with an email address and a unique identifier (UID).
  It includes a custom string representation for better readability.

Attributes:
- email_address (str): The email address of the user.
- uid (str): A unique identifier for the user. Defaults to an empty string.
  The `uid` field is excluded from the `repr` output and from comparisons between `User` instances.

Methods:
- __str__() -> str: Returns a string representation of the `User` instance,
  showing the user's email address in a formatted way.

Example usage:
    user = User(email_address="user@example.com", uid="12345")
    print(user)  # Output: User[user@example.com]
"""

# Builtin imports
from dataclasses import dataclass

# Local imports
from ..abstracts.abstract_model import AbstractRecommendModel
from . import constants as Key


@dataclass(frozen=True, kw_only=True)
class User(AbstractRecommendModel):
    """
    Represents a user with an email address and a unique identifier (UID).
    It includes a custom string representation for better readability.

    Args:
        email_address (str): The email address of the user.
    """

    email_address: str

    ###########################################################################
    # Property
    ###########################################################################
    @property
    def type(self) -> str:
        """Return the type of this model"""
        return Key.RECOMMEND_MODEL_USER

    ###########################################################################
    # Dunders
    ###########################################################################
    def __str__(self) -> str:
        """
        Returns a string representation of the `User` instance, showing the
        user's email address in a formatted way.
        """
        return f"User[{self.email_address}]"
