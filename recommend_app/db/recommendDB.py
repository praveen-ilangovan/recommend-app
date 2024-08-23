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


# class TRecommendDB():
#     def __init__(self, client: pymongo.MongoClient):
#         self.__client = client
#         self.__db = self.__client[Key.RECOMMEND_DATABASE]

#         self.__users = self.__db[Key.USERS_COLLECTION]
#         print(self.__users)
#         self.__users.create_index([(Key.USER_EMAIL_ADDRESS, pymongo.ASCENDING)], unique=True)

#     ###########################################################################
#     # Methods: User
#     ###########################################################################
#     def add_user(self, email_address: str) -> None:
#         """ Adds a new user to the db.

#         Args:
#             email_address (str): Email address of the user
#         """
#         return self.__users.insert_one({Key.USER_EMAIL_ADDRESS: email_address}).inserted_id

#     def get_user_by_id(self, id: str) -> None:
#         return self.__users.find_one({"_id": ObjectId(id)})

#     def get_user_by_index(self, email_address) -> None:
#         return self.__users.find_one({Key.USER_EMAIL_ADDRESS: email_address})


# class TUsers:
#     def __init__(self, db):
#         self.__collection = self.__db[Key.USERS_COLLECTION]
#         self.__collection.create_index([(Key.USER_EMAIL_ADDRESS, pymongo.ASCENDING)], unique=True)

#     def add(self, email_address):
#         """
#         """

#     def get_by_id(self, id):
#         """
#         """

#     def get_by_index(self, email_address):
#         """
#         """

#     def remove(self, email_address):
#         """
#         """
