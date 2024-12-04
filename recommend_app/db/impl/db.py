"""
Module: db.impl.db
==================

Implements the MongoDB database integration for the RecommendApp.

This module defines the `RecommendDB` class, which provides a MongoDB-backed
implementation of the `AbstractRecommendDB` interface. It manages the
connection to the MongoDB instance, interacts with collections, and performs
CRUD operations for the models used in the application.

Environment Variables:
- `DB_URL`: MongoDB connection URI with placeholders for user credentials.
- `DB_USER_ID`: MongoDB username for authentication.
- `DB_PASSWORD`: MongoDB password for authentication.
- `DB_SERVERSELECTIONTIMEOUT`: (Optional) Timeout for MongoDB server selection
                               in milliseconds.

Dependencies:
- `motor`: Async client for MongoDB
"""

# Builtin imports
import os
from typing import TYPE_CHECKING, Optional, Any

# Project specific imports
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import OperationFailure, DuplicateKeyError, InvalidOperation
from pydantic import ValidationError
import beanie

# Local imports
from ..abstracts.abstract_db import AbstractRecommendDB
from ..exceptions import (
    RecommendDBConnectionError,
    RecommendDBModelCreationError,
    RecommendAppDbError,
    RecommendDBModelNotFound,
)
from ..types import RecommendModelType
from .documents.user import UserDocument
from .documents.board import BoardDocument
from .documents.card import CardDocument

if TYPE_CHECKING:
    from motor.motor_asyncio import AsyncIOMotorDatabase
    from .documents.base import AbstractRecommendDocument
    from ..models.bases import (
        BaseNewRecommendModel,
        BaseRecommendModel,
        BaseUpdateRecommendModel,
    )


class RecommendDB(AbstractRecommendDB):
    """
    An asyncronous recommendDB using MongoDB and Motor client
    """

    def __init__(self, dbname: str):
        """
        Initialize the RecommendDB with MongoDB implementation.

        Args:
            dbname (str): Name of the database to be created/queried.
        """
        super().__init__()
        self.__dbname = dbname

        self.__db: Optional["AsyncIOMotorDatabase"] = None
        # Beanie Documents
        self.__documents: dict[
            RecommendModelType, type["AbstractRecommendDocument"]
        ] = {}

    ###########################################################################
    # Properties
    ###########################################################################
    @property
    def _db(self) -> Optional["AsyncIOMotorDatabase"]:
        """
        Returns the instance of MongoDB object.

        Returns:
            MongoDB: Pointer to the PyMongoDB instance.
        """
        return self.__db

    ###########################################################################
    # Methods: Connection
    ###########################################################################
    async def connect(self) -> bool:
        """
        Establishes a connection to the MongoDB database.

        This method retrieves the MongoDB connection URL and credentials from
        environment variables, attempts to connect to the MongoDB instance, and
        initializes the database collections.

        Returns:
            bool: True if the connection is successful, False otherwise.

        Raises:
            RecommendDBConnectionError: If the connection to the database fails.
        """
        try:
            db_url = os.environ["DB_URL"]
            db_user_id = os.environ["DB_USER_ID"]
            db_pwd = os.environ["DB_PASSWORD"]
        except KeyError as err:
            raise RecommendDBConnectionError("Failed to connect to the DB") from err

        url = db_url.format(USER=db_user_id, PWD=db_pwd)

        # Create a new client and connect to the server
        # Check if custom timeout is set.
        serverSelectionTimeoutMS = os.getenv("DB_SERVERSELECTIONTIMEOUT")
        if serverSelectionTimeoutMS is not None:
            client: AsyncIOMotorClient = AsyncIOMotorClient(
                url, serverSelectionTimeoutMS=int(serverSelectionTimeoutMS)
            )
        else:
            client = AsyncIOMotorClient(url)

        self.__db = client.get_database(self.__dbname)

        self.__documents[RecommendModelType.USER] = UserDocument
        self.__documents[RecommendModelType.BOARD] = BoardDocument
        self.__documents[RecommendModelType.CARD] = CardDocument

        # Init beanie
        await beanie.init_beanie(
            database=self.__db, document_models=list(self.__documents.values())
        )

        # Check the connection
        await self.ping()

        return True

    async def ping(self) -> bool:
        """
        Checks if the connection is successful

        Raises:
            RecommendDBConnectionError
        """
        if self.__db is None:
            return False

        try:
            await self.__db.client.admin.command("ping")
        except (OperationFailure, InvalidOperation) as err:
            raise RecommendDBConnectionError("Failed to connect to the DB") from err

        return True

    async def disconnect(self, clear_db: bool = False) -> bool:
        """
        Removes the connection to the database.

        Args:
            clear_db (bool): For testing. Clears the db while closing the connection

        Returns:
            True if the connection is disconnected
        """
        if self.__db is None:
            return False

        if clear_db:
            await self.__db.client.drop_database(self.__dbname)

        self.__db.client.close()

        return True

    ###########################################################################
    # Methods: CRUD
    ###########################################################################
    async def add(self, model: "BaseNewRecommendModel") -> "BaseRecommendModel":
        """
        Add a new model to the database.

        Args:
            model (BaseNewRecommendModel): Model to be added.

        Returns:
            BaseRecommendModel: The newly created model instance.

        Raises:
            `RecommendAppDbError` - General db error
            `RecommendDBModelCreationError` - The class that implements this
            method must throw this exception if the model creation failed.
        """
        doc_inst = self.__get_doc_inst(model.model_type)
        document = doc_inst.from_model(model)
        try:
            await document.create()
        except DuplicateKeyError as err:
            raise RecommendDBModelCreationError(
                f"{model.model_type.value} already exists"
            ) from err

        return document.to_model()

    async def get(
        self, model_type: "RecommendModelType", attrs_dict: dict[str, str]
    ) -> "BaseRecommendModel":
        """
        Retrieve a single model from the database that matches the given
        criteria.

        Args:
            model_type (RecommendModelType): The type of the model to retrieve
                                             (e.g., User, Board, Card).
            attrs_dict (dict[str, Any]): A dictionary of attributes to filter
                                         the model by.

        Returns:
            BaseRecommendModel: The model instance that matches the given criteria.

        Raises:
            `RecommendAppDbError` - General db error
            `RecommendDBModelNotFound` - The class that implements this
            method must throw this exception if the model is not found.
        """
        result = await self.__get_document(model_type, attrs_dict)
        return result.to_model()

    async def get_all(
        self, model_type: "RecommendModelType", attrs_dict: dict[str, Any]
    ) -> list["BaseRecommendModel"]:
        """
        Retrieves all documents matching criteria from the specified MongoDB
        collection.

        This method fetches multiple documents from the appropriate collection
        based on the model type and the provided criteria.

        Args:
            model_type (RecommendModelType): The type of model to retrieve.
            attrs_dict (dict[str, str]): A dictionary of attributes to match
                the documents.

        Returns:
            list[BaseRecommendModel]: A list of retrieved model instances.
        """
        doc_inst = self.__get_doc_inst(model_type)

        # TODO: Do Pagination (MongoDb Aggregation)
        docs = await doc_inst.find(attrs_dict).to_list()
        return [doc_inst.to_model(doc) for doc in docs]

    async def update(
        self, obj_id: str, update_model: "BaseUpdateRecommendModel"
    ) -> "BaseRecommendModel":
        """
        Updates the model in the database with the provided data. Only the non
        None data is updated.

        Args:
            obj_id (str): Id of the object to be updated.
            update_model (BaseUpdateRecommendModel): Data to be updated.

        Returns:
            BaseRecommendModel: The model instance that matches the given criteria.

        Raises:
            `RecommendDBModelNotFound` if the board is not found
            `RecommendAppDbError` if there is an issue in updating the model
        """
        doc = await self.__get_document(update_model.model_type, {"id": obj_id})

        # Filter out non-None values
        update_data = {
            key: value
            for key, value in update_model.model_dump().items()
            if value is not None
        }
        result = await doc.set(update_data)
        return result.to_model()

    async def remove(self, model_type: "RecommendModelType", obj_id: str) -> bool:
        """
        Remove a document from the database.

        Args:
            model_type (RecommendModelType): The type of the model to delete
                                             (e.g., User, Board, Card).
            obj_id (str): Id of the object to be deleted.

        Returns:
            bool: True if the document was successfully removed, False otherwise.
        """
        doc = await self.__get_document(model_type, {"id": obj_id})
        result = await doc.delete()
        return result.deleted_count == 1 if result else False

    ###########################################################################
    # Methods: privates
    ###########################################################################
    async def __get_document(
        self, model_type: "RecommendModelType", attrs_dict: dict[str, str]
    ) -> "AbstractRecommendDocument":
        """
        Retrieve a single document from the database that matches the given
        criteria.

        Args:
            model_type (RecommendModelType): The type of the model to retrieve
                                             (e.g., User, Board, Card).
            attrs_dict (dict[str, Any]): A dictionary of attributes to filter
                                         the model by.

        Returns:
            AbstractRecommendDocument

        Raises:
            `RecommendAppDbError` - General db error
            `RecommendDBModelNotFound` - The class that implements this
            method must throw this exception if the model is not found.
        """
        doc_inst = self.__get_doc_inst(model_type)

        if "id" in attrs_dict.keys():
            try:
                result = await doc_inst.get(attrs_dict["id"])
            except ValidationError:
                raise RecommendDBModelNotFound(
                    f"No {model_type.value} found for {attrs_dict}"
                )
        else:
            result = await doc_inst.find_one(attrs_dict)

        if not result:
            raise RecommendDBModelNotFound(
                f"No {model_type.value} found for {attrs_dict}"
            )

        return result

    def __get_doc_inst(
        self, model_type: "RecommendModelType"
    ) -> type["AbstractRecommendDocument"]:
        """
        Return the doc inst for the requested model type.

        Args:
            model_type (RecommendModelType): The type of the model to retrieve
                                             (e.g., User, Board, Card).

        Returns:
            An instance of the Document

        Raises:
            `RecommendAppDbError` - The class that implements this
            method must throw this exception if the model is not found.
        """
        inst = self.__documents.get(model_type)
        if not inst:
            raise RecommendAppDbError(
                f"{model_type.value} has no compatible beanie document type"
            )
        return inst
