"""
Module: abstract_colletion
==========================

This module defines the `AbstractCollection` class for interacting with
MongoDB collections.

The `AbstractCollection` class is an abstract base class that provides a template
for managing MongoDB collections. It includes methods for adding, finding, and
removing documents, as well as handling MongoDB-specific operations like indexing
and converting document formats.

Classes inheriting from `AbstractCollection` should implement the `model_type`
property to specify the type of model being managed by the collection.

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
    """
    Abstract base class for managing MongoDB collections in the RecommendApp.

    The `AbstractCollection` class provides methods for interacting with a MongoDB
    collection, including adding documents, finding single or multiple documents,
    and removing documents. It also handles conversion between MongoDB-specific
    fields (e.g., ObjectId) and the attributes used by RecommendModel instances.

    Attributes:
        _db (pymongo.database.Database): The MongoDB database instance.
        _collection (pymongo.collection.Collection): The specific MongoDB collection
        associated with this class.

    Subclasses must implement:
        - `model_type`: Specifies the `RecommendModelType` handled by the
        collection.
    """

    def __init__(self, db: "MongoDB"):
        """
        Initializes the `AbstractCollection` with the given MongoDB database
        instance.

        Args:
            db (pymongo.database.Database): The MongoDB database instance.

        The collection is automatically initialized based on the class name.
        """
        super().__init__()
        self.__db = db
        self.__collection = self.__db[self.collection_name]

    ###########################################################################
    # abstracts
    ###########################################################################
    @property
    def collection_name(self) -> str:
        """
        Returns the name of the MongoDB collection associated with this class.

        The collection name defaults to the class name of the inheriting class.

        Returns:
            str: The name of the MongoDB collection.
        """
        return self.__class__.__name__

    @property
    @abstractmethod
    def model_type(self) -> RecommendModelType:
        """
        Abstract property that must be implemented by subclasses to specify the
        model type.

        Returns:
            RecommendModelType: The type of model handled by this collection.

        Raises:
            NotImplementedError: If the subclass does not implement this
            property.
        """

    ###########################################################################
    # Methods
    ###########################################################################
    def create_index(self, keys: list[str], unique: bool = False) -> None:
        """
        Creates an index on the specified fields in the MongoDB collection.

        This method constructs and applies the index to the MongoDB collection.

        Args:
            keys (list[str]): The fields to index.
            unique (bool): Whether the index should enforce uniqueness.
        """
        index_list = [(key, pymongo.ASCENDING) for key in keys]
        self.__collection.create_index(index_list, unique=unique)

    def add(self, attrs_dict: dict[str, Any]) -> RecommendModel:
        """
        Adds a document to the MongoDB collection.

        Args:
            attrs_dict (dict[str, Any]): The attributes of the document to be
                added.

        Returns:
            RecommendModel: The model instance created from the document.

        Raises:
            RecommendDBModelCreationError: If a duplicate key error occurs
                during insertion.
        """
        try:
            self.__collection.insert_one(attrs_dict)
            # dict cleanup
            self.__mongo_to_attrs_dict(attrs_dict)
            return create_model(self.model_type, attrs_dict)
        except pymongo.errors.DuplicateKeyError as err:
            raise RecommendDBModelCreationError(err) from err

    def find_one(self, attrs_dict: dict[str, Any]) -> RecommendModel:
        """
        Finds a single document in the MongoDB collection based on the given
        attributes.

        Args:
            attrs_dict (dict[str, Any]): The attributes to filter the document.

        Returns:
            `RecommendModel`: The model instance corresponding to the found
                document.

        Raises:
            `RecommendDBModelNotFound`: If no document matches the given
                attributes.
        """
        self.__attrs_dict_to_mongo(attrs_dict)

        result = self.__collection.find_one(attrs_dict)
        if result:
            self.__mongo_to_attrs_dict(result)
            return create_model(self.model_type, result)

        msg = f"No result found. ModelType: {self.model_type}. Fields: {attrs_dict}"
        raise RecommendDBModelNotFound(msg)

    def find_all(self, attrs_dict: dict[str, Any]) -> list[RecommendModel]:
        """
        Finds multiple documents in the MongoDB collection based on the given
        attributes.

        Args:
            attrs_dict (dict[str, Any]): The attributes to filter the documents.

        Returns:
            list[RecommendModel]: A list of model instances corresponding to
                the found documents.

        Raises:
            `RecommendDBModelNotFound`: If no documents match the given attributes.
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
        Removes a document from the MongoDB collection based on the given
        attributes.

        Args:
            attrs_dict (dict[str, Any]): The attributes to identify the document
                to remove.

        Returns:
            bool: True if a document was successfully removed, False otherwise.
        """
        self.__attrs_dict_to_mongo(attrs_dict)
        return self.__collection.delete_one(attrs_dict).deleted_count != 0

    ###########################################################################
    # Methods: private
    ###########################################################################
    def __get_object_id(self, _id: str) -> Optional[ObjectId]:
        """
        Converts a string into a MongoDB ObjectId.

        Args:
            _id (str): The string representation of the ObjectId.

        Returns:
            Optional[ObjectId]: The corresponding ObjectId, or None if
                conversion fails.

        Raises:
            `RecommendDBModelNotFound`: If the string cannot be converted to an
                ObjectId.
        """
        try:
            return ObjectId(_id)
        except (TypeError, InvalidId) as err:
            raise RecommendDBModelNotFound(err) from err

    def __attrs_dict_to_mongo(self, attr_dict):
        """
        Converts the RecommendModel UID in the attributes dictionary to a
        MongoDB ObjectId.

        The method replaces the UID field with the corresponding MongoDB ObjectId.

        Args:
            attr_dict (dict[str, Any]): The attributes dictionary to be converted.
        """
        if ModelsKey.RECOMMEND_MODEL_ATTR_UID in attr_dict:
            object_id = self.__get_object_id(
                attr_dict[ModelsKey.RECOMMEND_MODEL_ATTR_UID]
            )
            attr_dict[Key.ATTR_ID] = object_id
            del attr_dict[ModelsKey.RECOMMEND_MODEL_ATTR_UID]

    def __mongo_to_attrs_dict(self, result):
        """
        Converts the MongoDB ObjectId in the result dictionary back to a
        RecommendModel UID.

        The method replaces the ObjectId field with the corresponding
        RecommendModel UID.

        Args:
            result (dict[str, Any]): The result dictionary to be converted.
        """
        if Key.ATTR_ID in result:
            result[ModelsKey.RECOMMEND_MODEL_ATTR_UID] = str(result[Key.ATTR_ID])
            del result[Key.ATTR_ID]
