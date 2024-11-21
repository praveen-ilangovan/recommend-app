# Builtin imports
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

# Project specific imports
import pymongo

# Local imports
from . import constants as Key
from ..db_client.models import RecommendModelType, RecommendModel, create_model
from ..db_client.models import constants as ModelsKey
from ..db_client.exceptions import (
    RecommendDBModelCreationError,
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

    async def add(self, attrs_dict: dict[str, Any]) -> RecommendModel:
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
            await self.__collection.insert_one(attrs_dict)
            # dict cleanup
            self.__mongo_to_attrs_dict(attrs_dict)
            return create_model(self.model_type, attrs_dict)
        except pymongo.errors.DuplicateKeyError as err:
            raise RecommendDBModelCreationError(err) from err

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
