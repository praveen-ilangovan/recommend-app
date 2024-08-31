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
from ..db_client.models import constants as ModelsKey
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
    def collection_name(self) -> str:
        """Returns the name of the collection"""
        return self.__class__.__name__

    @property
    @abstractmethod
    def model_type(self) -> RecommendModelType:
        """Returns the name of the model type this class handles"""

    ###########################################################################
    # Methods
    ###########################################################################
    def create_index(self, keys: list[str], unique: bool = False) -> None:
        """Make the key an index. If unique is set to True, make it a unique
        index.

        Args:
            key (str): Key to be made an index
            unique (bool): If true, a unique index is created. Default: False.
        """
        index_list = [(key, pymongo.ASCENDING) for key in keys]
        self.__collection.create_index(index_list, unique=unique)

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
            self.__collection.insert_one(attrs_dict)
            # dict cleanup
            self.__mongo_to_attrs_dict(attrs_dict)
            return create_model(self.model_type, attrs_dict)
        except pymongo.errors.DuplicateKeyError as err:
            raise RecommendDBModelCreationError(err) from err

    def find_one(self, attrs_dict: dict[str, Any]) -> RecommendModel:
        """Find the document using its attributes

        Args:
            attrs_dict (dict): A dictionary of key-value pairs.

        Returns:
            dict
        """
        self.__attrs_dict_to_mongo(attrs_dict)

        result = self.__collection.find_one(attrs_dict)
        if result:
            self.__mongo_to_attrs_dict(result)
            return create_model(self.model_type, result)

        msg = f"No result found. ModelType: {self.model_type}. Fields: {attrs_dict}"
        raise RecommendDBModelNotFound(msg)

    def find_all(self, attrs_dict: dict[str, Any]) -> list[RecommendModel]:
        """Find all the documents matching the attributes

        Args:
            attrs_dict (dict): A dictionary of key-value pairs.

        Returns:
            list[RecommendModel]
        """
        entities: list[RecommendModel] = []

        self.__attrs_dict_to_mongo(attrs_dict)
        result = self.__collection.find(attrs_dict)

        for entity in result:
            self.__mongo_to_attrs_dict(entity)
            entities.append(create_model(self.model_type, entity))

        if not entities:
            msg = f"No result found. ModelType: {self.model_type}. Fields: {attrs_dict}"
            raise RecommendDBModelNotFound(msg)

        return entities

    def remove(self, attrs_dict: dict[str, Any]) -> bool:
        """
        Remove a document from the database

        Args:
            attrs_dict (dict): A dictionary of key-value pairs.

        Returns:
            True if the item is removed.
        """
        self.__attrs_dict_to_mongo(attrs_dict)
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
            raise RecommendDBModelNotFound(err) from err

    def __attrs_dict_to_mongo(self, attr_dict):
        """
        Change key uid to _id
        Then convert the value of _id to ObjectID
        Delete uid
        """
        if ModelsKey.RECOMMEND_MODEL_ATTR_ID in attr_dict:
            object_id = self.__get_object_id(
                attr_dict[ModelsKey.RECOMMEND_MODEL_ATTR_ID]
            )
            attr_dict[Key.ATTR_ID] = object_id
            del attr_dict[ModelsKey.RECOMMEND_MODEL_ATTR_ID]

    def __mongo_to_attrs_dict(self, result):
        """
        Change key _id to uid
        Convert the value to string
        Delete _id
        """
        if Key.ATTR_ID in result:
            result[ModelsKey.RECOMMEND_MODEL_ATTR_ID] = str(result[Key.ATTR_ID])
            del result[Key.ATTR_ID]
