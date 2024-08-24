"""
Collection that holds all the users documents
"""

# Builtin imports
from typing import TYPE_CHECKING

# Local imports
from ..abstracts import AbstractCollection
from .. import constants as Key
from ..models.user import User

if TYPE_CHECKING:
    from ..typealiases import MongoDatabase


class Users(AbstractCollection):
    def __init__(self, db: "MongoDatabase"):
        super().__init__(db)

        # Make email address a unique key
        self.create_index(Key.USER_EMAIL_ADDRESS, unique=True)

    ###########################################################################
    # Properties
    ###########################################################################
    @property
    def collection_name(self) -> str:
        """Returs the name of this collection"""
        return Key.COL_USERS

    ###########################################################################
    # Methods
    ###########################################################################
    def add(self, email_address: str) -> str:
        """
        Add a new user to the db using their email_address. This email address
        has to be unique.

        Args:
            email_address (str) : Email address of the user

        Returns:
            str : Unique ID of the newly created user

        Raises:
            RecommendDBDuplicateKeyError - If the email_address isn't unique.
        """
        return self._add(**{Key.USER_EMAIL_ADDRESS: email_address})

    def get(self, _id: str) -> User:
        """Get the user by their unique ID

        Args:
            _id (str) : ID of the user

        Returns:
            User
        """
        user_dict = self._find({Key.ATTR_ID: _id})
        return User(**user_dict)

    def get_by_email_address(self, email_address: str) -> "User":
        """
        Get the user from the database using their email address.

        Args:
            email_address (str) : User's email address

        Returns:
            User : user data
        """
        user_dict = self._find({"email_address": email_address})
        return User(**user_dict)

    def remove(self, user: "User") -> bool:
        """
        Remove the user from the database

        Args:
            user (User) : User to be removed

        Returns:
            True if user is removed
        """
        return self._remove({Key.ATTR_ID: user._id})
