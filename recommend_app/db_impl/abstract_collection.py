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

    def _add(self, **kwargs) -> Optional[str]:
        """Adds a new entry to the collection

        Please refer to the classes instancing this class for arguments.

        Returns:
            str : Unique ID of the created entry or None
        """
        try:
            return self.__collection.insert_one(kwargs).inserted_id
        except pymongo.errors.DuplicateKeyError:
            return None

    def _find(self, attrs_dict: dict[str, Any]) -> Optional[dict[str, Any]]:
        """Find the document using its attributes

        Args:
            attrs_dict (dict): A dictionary of key-value pairs.

        Returns:
            dict
        """
        if Key.ATTR_ID in attrs_dict:
            attrs_dict[Key.ATTR_ID] = self.__get_object_id(attrs_dict[Key.ATTR_ID])

        result = self.__collection.find_one(attrs_dict)
        if result:
            result["uid"] = result[Key.ATTR_ID]
            del result[Key.ATTR_ID]

        return result

    def _remove(self, attrs_dict: dict[str, Any]) -> bool:
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
        except (TypeError, InvalidId):
            return None
