"""
Module that manages the app's db. Exposes methods to add, get and remove
users, boards and cards.
"""

# Builtin imports
import os
from typing import TYPE_CHECKING

# Project specific imports
from pymongo import MongoClient
from pymongo.errors import InvalidURI, OperationFailure, ServerSelectionTimeoutError

# Local imports
from . import constants as Key
from .collections.users import Users
from .exceptions import RecommendDBConnectionError

if TYPE_CHECKING:
    from .typealiases import MongoDatabase
    from .models.user import User


class RecommendDB:
    """
    RecommendDB exposes methods to add, get and remove users, boards and cards.
    """

    def __init__(self, db: "MongoDatabase"):
        self.__db = db

        # Collections
        self.__users = Users(self.__db)

    @classmethod
    def connect(cls, dbname: str = Key.DB_NAME) -> "RecommendDB":
        """Connect to the database and return the instance

        Connects to the MongoDB Cluster using the URL defined in the constants.
        The user_id and password are grabbed from the environment variables.
        Upon connecting to the cluster, the database is created (if it doesn't
        already exist. Technically, mongo doesn't create a db until a document
        is added to a collection within this db.)

        Args:
            dbname (str): Name of the database to connect

        Returns:
            RecommendDB: An instance of this class

        Raises:
            RecommendDBConnectionError
        """
        url = os.environ["DB_URL"].format(
            USER=os.getenv("DB_USER_ID"), PWD=os.getenv("DB_PASSWORD")
        )

        try:
            # Check if custom timeout is set.
            serverSelectionTimeoutMS = os.getenv("DB_SERVERSELECTIONTIMEOUT")
            if serverSelectionTimeoutMS is not None:
                client: MongoClient = MongoClient(
                    url, serverSelectionTimeoutMS=int(serverSelectionTimeoutMS)
                )
            else:
                client = MongoClient(url)

            # Do this to make sure the connection is established. This throws
            # an exception if there is no connection.
            client.server_info()
            return cls(client[dbname])

        except (InvalidURI, OperationFailure, ServerSelectionTimeoutError) as err:
            raise RecommendDBConnectionError from err

    ###########################################################################
    # Properties
    ###########################################################################
    @property
    def _db(self) -> "MongoDatabase":
        """Returns the instance of the MongoDB"""
        return self.__db

    ###########################################################################
    # Methods: Users
    ###########################################################################
    def add_user(self, email_address: str) -> str:
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
        return self.__users.add(email_address)

    def get_user(self, _id: str) -> "User":
        """
        Get the user from the database using their uniqueID.

        Args:
            _id (str) : User's unique ID

        Returns:
            User : user data
        """
        return self.__users.get(_id)

    def get_user_by_email_address(self, email_address: str) -> "User":
        """
        Get the user from the database using their email address.

        Args:
            email_address (str) : User's email address

        Returns:
            User : user data
        """
        return self.__users.get_by_email_address(email_address)

    def remove_user(self, user: "User") -> bool:
        """
        Remove the user from the database

        Args:
            user (User) : User to be removed

        Returns:
            True if user is removed
        """
        return self.__users.remove(user)
