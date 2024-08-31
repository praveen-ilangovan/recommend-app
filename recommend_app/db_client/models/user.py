"""
Module: user
============

This module defines the `User` model, which represents a user in the
recommend_app. The `User` model inherits from the `AbstractRecommendModel`
class, ensuring that it follows a consistent structure defined for all models
in the application. Each `User` instance is immutable and identified by a
unique identifier (UID) and an email address.

The `User` model is crucial for managing user-related data, such as storing
user information and associating users with boards and recommendations within
the app.
"""

# Builtin imports
from dataclasses import dataclass

# Local imports
from ..abstracts.abstract_model import AbstractRecommendModel
from . import constants as Key


@dataclass(frozen=True, kw_only=True)
class User(AbstractRecommendModel):
    """
    Model representing a user in the recommend_app.

    This class inherits from `AbstractRecommendModel` and represents a user
    entity with a unique identifier (UID) and an associated email address.
    The class is immutable (due to `frozen=True`), ensuring that instances
    cannot be modified after creation, which helps maintain consistency and
    data integrity.

    Attributes:
        email_address (str): The email address associated with the user.
    """

    email_address: str

    ###########################################################################
    # Property
    ###########################################################################
    @property
    def type(self) -> str:
        """
        Returns the type of the model, which is 'User'.

        This property overrides the abstract `type` property from the
        `AbstractRecommendModel` class.

        Returns:
            str: The string constant representing the type of the model, 'User'.
        """
        return Key.RECOMMEND_MODEL_USER

    ###########################################################################
    # Dunders
    ###########################################################################
    def __str__(self) -> str:
        """
        Returns a string representation of the User instance.

        The string includes the model type ('User') and the user's email
        address in the format: 'User: [email_address]'.

        Returns:
            str: A string representation of the User instance.
        """
        return f"{self.type}: [{self.email_address}]"
