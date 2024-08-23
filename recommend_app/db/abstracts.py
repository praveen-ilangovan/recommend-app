"""
Holds the abstract classes used in the recommend_app.db module
"""

# Builtin imports
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

# Project specific imports
import pymongo
import pymongo.errors

# Local imports
from .exceptions import RecommendDBDuplicateKeyError

if TYPE_CHECKING:
    from .typealiases import MongoDatabase


class AbstractCollection(ABC):
    def __init__(self, db: "MongoDatabase"):
        super().__init__()
        self.__db = db
        self.__collection = self.__db[self.collection_name]

    ###########################################################################
    # abstracts
    ###########################################################################
    @property
    @abstractmethod
    def collection_name(self) -> str:
        """Returns the name of the collection"""

    ###########################################################################
    # Properties
    ###########################################################################
    @property
    def db(self) -> "MongoDatabase":
        """Returns the db instance"""
        return self.__db

    @property
    def collection(self):
        """Returns the collection instance"""
        return self.__collection

    ###########################################################################
    # Methods
    ###########################################################################
    def create_index(self, key: str, unique: bool = False) -> None:
        """Make the key an index. If unique is set to True, make it a unique
        index.

        Args:
            key (str): Key to be made an index
            unique (bool): If true, a unique index is created. Default: False.
        """
        self.__collection.create_index([(key, pymongo.ASCENDING)], unique=unique)

    def _add(self, **kwargs) -> str:
        """Adds a new entry to the collection

        Please refer to the classes instancing this class for arguments.

        Returns:
            str : Unique ID of the created entry.

        Raises:
            RecommendDBDuplicateKeyError
        """
        try:
            return self.__collection.insert_one(kwargs).inserted_id
        except pymongo.errors.DuplicateKeyError as err:
            raise RecommendDBDuplicateKeyError(
                "Document with this unique index already exists"
            ) from err
