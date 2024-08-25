"""
module: db
"""

# Builtin imports
import os
from typing import TYPE_CHECKING, Optional

# Project specific imports
from pymongo import MongoClient
from pymongo.errors import (
    InvalidURI,
    OperationFailure,
    ServerSelectionTimeoutError,
    ConfigurationError,
)

# Local imports
from .collections.users import Users
from ..db_client.abstract_db import AbstractRecommendDB
from ..db_client.models.user import User

if TYPE_CHECKING:
    from pymongo.database import Database as MongoDB


class RecommendDB(AbstractRecommendDB):
    def __init__(self, dbname: str):
        super().__init__()
        self.__dbname = dbname
        self.__db: Optional["MongoDB"] = None
        self.__users: Optional[Users] = None

    ###########################################################################
    # Properties
    ###########################################################################
    @property
    def _db(self) -> Optional["MongoDB"]:
        """Returns the instance of the database"""
        return self.__db

    ###########################################################################
    # Methods
    ###########################################################################
    def connect(self) -> bool:
        """
        Establishes connection to the database.

        Connects to the MongoDB Cluster using the environment variables DB_URL,
        DB_USER_ID and DB_PASSWORD. Upon connecting to the cluster,
        the database is created (if it doesn't already exist. Technically,
        mongo doesn't create a db until a document is added to a collection
        within this db).

        Returns:
            True if the connection is successful.
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
            self.__initialize(client[self.__dbname])

            return True

        except (
            InvalidURI,
            OperationFailure,
            ServerSelectionTimeoutError,
            ConfigurationError,
        ):
            return False

    def add_user(self, email_address: str) -> Optional[User]:
        """
        Add a new user to the db using their email_address. This email address
        has to be unique.

        Args:
            email_address (str) : Email address of the user

        Returns:
            User or None
        """
        if not self.__users:
            return None
        return self.__users.add(email_address)

    def get_user(self, uid: str) -> Optional[User]:
        """
        Get the user from the database using their uniqueID.

        Args:
            uid (str) : User's unique ID

        Returns:
            User
        """
        if not self.__users:
            return None
        return self.__users.get(uid)

    def get_user_by_email_address(self, email_address: str) -> Optional[User]:
        """
        Get the user from the database using their email address.

        Args:
            email_address (str) : User's email address

        Returns:
            User : user data
        """
        if not self.__users:
            return None
        return self.__users.get_by_email_address(email_address)

    def remove_user(self, user: User) -> bool:
        """
        Remove the user from the database

        Args:
            user (User) : User to be removed

        Returns:
            True if user is removed
        """
        if not self.__users:
            return False
        return self.__users.remove(user)

    ###########################################################################
    # Methods: Privates
    ###########################################################################
    def __initialize(self, db: "MongoDB") -> None:
        """
        Initializes the db and collections
        """
        self.__db = db
        self.__users = Users(self.__db)
