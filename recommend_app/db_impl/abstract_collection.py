"""
Abstract collection
"""

# Builtin imports
from abc import ABC, abstractmethod
from bson.objectid import ObjectId
from bson.errors import InvalidId
from typing import TYPE_CHECKING, Optional, Any

# Project specific imports
import pymongo

# Local imports
from . import constants as Key
from ..db_client.models import RecommendModelType, RecommendModel, create_model
from ..db_client.exceptions import (
    RecommendDBModelCreationError,
    RecommendDBModelNotFound,
)

if TYPE_CHECKING:
    from pymongo.database import Database as MongoDB


class AbstractCollection(ABC):
    def __init__(self, db: "MongoDB"):
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

    @property
    @abstractmethod
    def model_type(self) -> RecommendModelType:
        """Returns the name of the model type this class handles"""

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

    def add(self, attrs_dict: dict[str, Any]) -> RecommendModel:
        """
        Adds a new document to the collection.

        Args:
            attrs_dict (dict): Key-value pairs.

        Returns:
            `RecommendModel` - `User` | `Board` | `Card`

        Raises:
            `RecommendDBModelCreationError` - The class that implements this
            method must throw this exception if the model creation failed.
        """
        try:
            uid = self.__collection.insert_one(attrs_dict).inserted_id

            # dict cleanup
            del attrs_dict["_id"]
            attrs_dict["uid"] = uid

            return create_model(self.model_type, attrs_dict)
        except pymongo.errors.DuplicateKeyError as err:
            raise RecommendDBModelCreationError from err

    def find_one(self, attrs_dict: dict[str, Any]) -> RecommendModel:
        """Find the document using its attributes

        Args:
            attrs_dict (dict): A dictionary of key-value pairs.

        Returns:
            dict
        """
        if "uid" in attrs_dict:
            attrs_dict["_id"] = self.__get_object_id(attrs_dict["uid"])
            del attrs_dict["uid"]

        result = self.__collection.find_one(attrs_dict)
        if result:
            result["uid"] = result[Key.ATTR_ID]
            del result[Key.ATTR_ID]
            return create_model(self.model_type, result)

        msg = f"No result found. ModelType: {self.model_type}. Fields: {attrs_dict}"
        raise RecommendDBModelNotFound(msg)

    def remove(self, attrs_dict: dict[str, Any]) -> bool:
        """
        Remove a document from the database

        Args:
            attrs_dict (dict): A dictionary of key-value pairs.

        Returns:
            True if the item is removed.
        """
        if Key.ATTR_ID in attrs_dict:
            attrs_dict[Key.ATTR_ID] = self.__get_object_id(attrs_dict[Key.ATTR_ID])

        return self.__collection.delete_one(attrs_dict).deleted_count != 0

    ###########################################################################
    # Methods: private
    ###########################################################################
    def __get_object_id(self, _id: str) -> Optional[ObjectId]:
        """
        Convert str id to ObjectId.

        Args:
            _id (str) : Unique ID

        Returns:
            ObjectId
        """
        try:
            return ObjectId(_id)
        except (TypeError, InvalidId) as err:
            raise RecommendDBModelNotFound from err
