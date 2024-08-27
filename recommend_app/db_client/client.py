"""
Module: recommend_db_client

This module contains the `RecommendDbClient` class, which provides a
higher-level interface to interact with the recommendation database.
The `RecommendDbClient` class abstracts operations such as connecting to the
database, adding, retrieving, and removing the users, boards and cards.

The class relies on an underlying database implementation that adheres to the
`AbstractRecommendDB` interface. This ensures flexibility and allows the
application to work with different database backends by providing a consistent
API.

Classes:
- RecommendDbClient: A wrapper class that interacts with the underlying database
  and handles common operations such as connecting, adding, retrieving, and
  removing users, boards and cards.

Example usage:
    from recommend_app.db_client.client import RecommendDbClient

    db_client = RecommendDbClient(db=SomeRecommendDB())
    db_client.connect()
    new_user = db_client.add_user("user@example.com")
    fetched_user = db_client.get_user(new_user.id)
    db_client.remove_user(fetched_user)

Exceptions:
- RecommendDBConnectionError: Raised when the database connection fails.
- RecommendDBModelCreationError: Raised when a model (e.g., user) creation fails.
- RecommendDBModelNotFound: Raised when a requested model is not found in the database.

Dependencies:
- AbstractRecommendDB: An abstract base class that the underlying database
  implementation must inherit from.
"""

# Builtin imports
from typing import TYPE_CHECKING, cast

# Local imports
from .models import RecommendModelType, User, Board
from .models import constants as Key
from .exceptions import RecommendDBConnectionError

if TYPE_CHECKING:
    from .abstracts.abstract_db import AbstractRecommendDB


class RecommendDbClient:
    """
    Provides interface to perform CRUD operations (i.e) add, get and remove
    users, boards and cards.

    Args:
        db (AbstractRecommendDB) : Child class inheriting this abstract class.
    """

    def __init__(self, db: "AbstractRecommendDB"):
        self.__db = db

    ###########################################################################
    # Methods
    ###########################################################################
    def connect(self) -> None:
        """
        Establishes connection to the database

        Raises:
            `RecommendDBConnectionError` if the connection fails.
        """
        status = self.__db.connect()
        if not status:
            raise RecommendDBConnectionError(
                f"Connection to {self.__db.__class__.__name__} failed."
            )

    ###########################################################################
    # Users
    ###########################################################################
    def add_user(self, email_address: str) -> User:
        """
        Add a new user to the db using their email_address. This email address
        has to be unique.

        Args:
            email_address (str) : Email address of the user

        Returns:
            User

        Raises:
            `RecommendDBModelCreationError` if user creation fails.
        """
        model = self.__db.add(
            RecommendModelType.USER, {Key.RECOMMEND_MODEL_ATTR_EMAIL: email_address}
        )
        user = cast(User, model)  # Type narrowing to keep static type checker happy.
        return user

    def get_user(self, uid: str) -> User:
        """
        Get the user from the database using their unique identifier.

        Args:
            uid (str) : User's unique ID

        Returns:
            User

        Raises:
            `RecommendDBModelNotFound` if the user is not found.
        """
        model = self.__db.get(
            RecommendModelType.USER, {Key.RECOMMEND_MODEL_ATTR_ID: uid}
        )
        user = cast(User, model)  # Type narrowing to keep static type checker happy.
        return user

    def get_user_by_email_address(self, email_address: str) -> User:
        """
        Get the user from the database using their email address.

        Args:
            email_address (str) : User's email address

        Returns:
            User

        Raises:
            `RecommendDBModelNotFound` if the user is not found.
        """
        model = self.__db.get(
            RecommendModelType.USER, {Key.RECOMMEND_MODEL_ATTR_EMAIL: email_address}
        )
        user = cast(User, model)  # Type narrowing to keep static type checker happy.
        return user

    def remove_user(self, user: User) -> bool:
        """
        Remove the user from the database

        Args:
            user (User) : User to be removed

        Returns:
            True if user is removed
        """
        return self.__db.remove(user)

    ###########################################################################
    # Boards
    ###########################################################################
    def add_board(self, name: str, user: User) -> Board:
        """
        Add a board to the database. Takes in the name of the board and the
        user who creates it. The name should be unique for the given user.

        Args:
            name (str): Name of the board
            user (User): User who creates and owns the board

        Returns:
            Board

        Raises:
            `RecommendDBModelCreationError` if board creation fails.
        """
        model = self.__db.add(
            RecommendModelType.BOARD,
            {
                Key.RECOMMEND_MODEL_ATTR_BOARD_NAME: name,
                Key.RECOMMEND_MODEL_ATTR_BOARD_OWNER_ID: user.uid,
            },
        )
        board = cast(Board, model)  # Type narrowing to keep static type checker happy.
        return board

    def get_board(self, uid: str) -> Board:
        """
        Get the board from the database using its unique identifier.

        Args:
            uid (str) : Board's unique ID

        Returns:
            Board

        Raises:
            `RecommendDBModelNotFound` if the user is not found.
        """
        model = self.__db.get(
            RecommendModelType.BOARD, {Key.RECOMMEND_MODEL_ATTR_ID: uid}
        )
        board = cast(Board, model)  # Type narrowing to keep static type checker happy.
        return board

    def get_board_by_name(self, name: str, user: User) -> Board:
        """
        Get the board by its name for the specified user.

        Args:
            uid (str) : Board's unique ID
            user (User): User who creates and owns the board

        Returns:
            Board

        Raises:
            `RecommendDBModelNotFound` if the board is not found.
        """
        model = self.__db.get(
            RecommendModelType.BOARD,
            {
                Key.RECOMMEND_MODEL_ATTR_BOARD_NAME: name,
                Key.RECOMMEND_MODEL_ATTR_BOARD_OWNER_ID: user.uid,
            },
        )
        board = cast(Board, model)  # Type narrowing to keep static type checker happy.
        return board
