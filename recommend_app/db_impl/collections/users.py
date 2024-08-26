"""
Collection that holds all the users documents
"""

# Builtin imports
from typing import TYPE_CHECKING, Optional

# Local imports
from ..abstract_collection import AbstractCollection
from .. import constants as Key
from ...db_client.models.user import User

if TYPE_CHECKING:
    from pymongo.database import Database as MongoDB


class Users(AbstractCollection):
    def __init__(self, db: "MongoDB"):
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
    def add(self, email_address: str) -> Optional[User]:
        """
        Add a new user to the db using their email_address. This email address
        has to be unique.

        Args:
            email_address (str) : Email address of the user

        Returns:
            User
        """
        uid = self._add(**{Key.USER_EMAIL_ADDRESS: email_address})
        return User(email_address=email_address, uid=uid) if uid else None

    def get(self, uid: str) -> Optional[User]:
        """Get the user by their unique ID

        Args:
            uid (str) : ID of the user

        Returns:
            User
        """
        result = self._find({Key.ATTR_ID: uid})
        return User(**result) if result else None

    def get_by_email_address(self, email_address: str) -> Optional[User]:
        """
        Get the user from the database using their email address.

        Args:
            email_address (str) : User's email address

        Returns:
            User
        """
        result = self._find({"email_address": email_address})
        return User(**result) if result else None

    def remove(self, user: User) -> bool:
        """
        Remove the user from the database

        Args:
            user (User) : User to be removed

        Returns:
            True if user is removed
        """
        return self._remove({Key.ATTR_ID: user.uid})
