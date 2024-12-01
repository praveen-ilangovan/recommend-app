"""
Module: db.client
========================

This module defines the `RecommendDbClient` class, which acts as a client for
interacting with the underlying database that stores the data for the
recommend_app. It handles operations related to users, boards, and cards,
including adding, retrieving, and removing entities. The `RecommendDbClient`
class abstracts away the direct interactions with the database, making it
easier to manage and extend the application's data storage layer.
"""

# Builtin imports
from typing import TYPE_CHECKING, Optional, cast

# Local imports
from .exceptions import RecommendDBConnectionError, RecommendAppDbError
from .types import RecommendModelType
from .hashing import Hasher
from .models.board import NewBoard

if TYPE_CHECKING:
    from .abstracts.abstract_db import AbstractRecommendDB
    from .models.user import NewUser, UserInDb
    from .models.board import BoardInDb


class RecommendDbClient:
    """
    A client class for managing operations related to users, boards, and cards
    in the recommend_app database.

    This class interacts with an abstract database layer defined by the
    `AbstractRecommendDB` interface. It provides methods to add, retrieve, and
    remove users, boards, and cards. The class also manages the connection to
    the database and handles exceptions related to database connectivity.

    Attributes:
        __db (AbstractRecommendDB): The database instance used for storage and
        retrieval of data.
    """

    def __init__(self, db: "AbstractRecommendDB"):
        """
        Initialize the RecommendDbClient with a specific database
        implementation.

        Args:
            db (AbstractRecommendDB): An instance of a class implementing the
                                      AbstractRecommendDB interface, which
                                      defines the database operations.
        """
        self.__db = db

    ###########################################################################
    # Methods: DB
    ###########################################################################
    async def connect(self) -> bool:
        """
        Establish a connection to the database.

        Returns:
            True if connection is successful.

        Raises:
            RecommendDBConnectionError: If the connection to the database fails.
        """
        status: bool = await self.__db.connect()
        if not status:
            raise RecommendDBConnectionError(
                f"Connection to {self.__db.__class__.__name__} failed."
            )
        return status

    async def ping(self) -> bool:
        """
        Checks the connection

        Returns:
            True if the connection exist
        """
        status = await self.__db.ping()
        return status

    async def disconnect(self, clear_db: bool = False) -> bool:
        """
        Disconnects the connection
        """
        status = await self.__db.disconnect(clear_db)
        return status

    ###########################################################################
    # Methods: User
    ###########################################################################
    async def add_user(self, new_user: "NewUser") -> "UserInDb":
        """
        Add a new user to the database.

        Args:
            new_user (NewUser): Data model that has the details of the new user
                including email_address, user_name, first and last_name and password.

        Returns:
            User: The newly created User object.

        Raises:
            `RecommendDBModelCreationError` if user creation fails.
        """
        # Hash the password
        new_user.password = Hasher.hash_password(new_user.password)
        result = await self.__db.add(new_user)
        return cast(
            "UserInDb", result
        )  # Type narrowing to keep static type checker happy.

    async def get_user(
        self,
        id: Optional[str] = None,
        email_address: Optional[str] = None,
        user_name: Optional[str] = None,
    ) -> "UserInDb":
        """
        Retrieve a user from the database by their unique attribute: id, email or username.

        Args:
            id (str): The unique identifier of the user.
            email_address (str): Email address of the user.
            user_name (str): User name of the user

        Returns:
            UserInDb: The User object corresponding to the provided UID.

        Raises:
            `RecommendAppDbError`
            `RecommendDBModelNotFound` if the user is not found.
        """
        attrs_dict = {}
        if id is not None:
            attrs_dict["id"] = id
        elif email_address is not None:
            attrs_dict["email_address"] = email_address
        elif user_name is not None:
            attrs_dict["user_name"] = user_name
        else:
            raise RecommendAppDbError(
                "Please provide an id or email or username of the user."
            )

        result = await self.__db.get(RecommendModelType.USER, attrs_dict)
        return cast("UserInDb", result)

    ###########################################################################
    # Methods: Board
    ###########################################################################
    async def add_board(self, new_board: NewBoard, owner_id: str) -> "BoardInDb":
        """
        Add a new board to the database, associated with a specific user.

        Args:
            new_board (NewBoard): Board model with all the necessary info to create a new board
            owner_id (str): User who is creating this board

        Returns:
            BoardInDb: The newly created Board object.

        Raises:
            `RecommendDBModelCreationError` if board creation fails.
        """
        board_with_ownerid = NewBoard(**new_board.model_dump(), owner_id=owner_id)
        result = await self.__db.add(board_with_ownerid)
        return cast("BoardInDb", result)

    async def get_board(
        self, board_id: str, owner_id: Optional[str] = None
    ) -> "BoardInDb":
        """
        Retrieve a board from the database by its unique identifier (UID).

        Args:
            board_id (str): The unique identifier of the board.
            owner_id (str): If the board is private, then owner_id must be
                provided. The board will be returned only if it belongs to the
                owner.

        Returns:
            Board: The Board object corresponding to the provided UID.

        Raises:
            `RecommendDBModelNotFound` if the board is not found
            `RecommendAppDbError` if the board is private and no owner_id is
                given or if the given owner_id doesn't match the board's owner.
        """
        attrs_dict = {"id": board_id}
        board = await self.__db.get(RecommendModelType.BOARD, attrs_dict)
        board = cast("BoardInDb", board)
        if board.private:
            if not owner_id:
                raise RecommendAppDbError(
                    f"Board with {board_id} is private. Please provide the owner_id"
                )
            if board.owner_id != owner_id:
                raise RecommendAppDbError(
                    "Owner doesn't have access to this private board."
                )

        return board

    async def get_all_boards(self, owner_id: str) -> list["BoardInDb"]:
        """
        Retrieve all boards associated with a specific user.

        Args:
            owner_id (str): The id of the owner whose boards are being queried

        Returns:
            list[Board]: A list of Board objects belonging to the user.
        """
        boards = await self.__db.get_all(
            RecommendModelType.BOARD, {"owner_id": owner_id}
        )
        return cast(list["BoardInDb"], boards)
