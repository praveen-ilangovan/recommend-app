"""
Module: client
==============

This module defines the `RecommendDbClient` class, which acts as a client for
interacting with the underlying database that stores the data for the
recommend_app. It handles operations related to users, boards, and cards,
including adding, retrieving, and removing entities. The `RecommendDbClient`
class abstracts away the direct interactions with the database, making it
easier to manage and extend the application's data storage layer.
"""

# Builtin imports
from typing import TYPE_CHECKING, cast

# Local imports
from .models import RecommendModelType, User, Board, Card
from .models import constants as Key
from .exceptions import RecommendDBConnectionError

if TYPE_CHECKING:
    from .abstracts.abstract_db import AbstractRecommendDB


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
    # Methods
    ###########################################################################
    def connect(self) -> None:
        """
        Establish a connection to the database.

        Raises:
            RecommendDBConnectionError: If the connection to the database fails.
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
        Add a new user to the database.

        Args:
            email_address (str): The email address of the user to be added.

        Returns:
            User: The newly created User object.

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
        Retrieve a user from the database by their unique identifier (UID).

        Args:
            uid (str): The unique identifier of the user.

        Returns:
            User: The User object corresponding to the provided UID.

        Raises:
            `RecommendDBModelNotFound` if the user is not found.
        """
        model = self.__db.get(
            RecommendModelType.USER, {Key.RECOMMEND_MODEL_ATTR_UID: uid}
        )
        user = cast(User, model)  # Type narrowing to keep static type checker happy.
        return user

    def get_user_by_email_address(self, email_address: str) -> User:
        """
        Retrieve a user from the database by their email address.

        Args:
            email_address (str): The email address of the user.

        Returns:
            User: The User object corresponding to the provided email address.

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
        Remove a user from the database.

        Args:
            user (User): The User object to be removed.

        Returns:
            bool: True if the user was successfully removed, False otherwise.
        """
        return self.__db.remove(user)

    ###########################################################################
    # Boards
    ###########################################################################
    def add_board(self, name: str, user: User) -> Board:
        """
        Add a new board to the database, associated with a specific user.

        Args:
            name (str): The name of the board to be created.
            user (User): The user who owns the board.

        Returns:
            Board: The newly created Board object.

        Raises:
            `RecommendDBModelCreationError` if board creation fails.
        """
        model = self.__db.add(
            RecommendModelType.BOARD,
            {
                Key.RECOMMEND_MODEL_ATTR_BOARD_NAME: name,
                Key.RECOMMEND_MODEL_ATTR_BOARD_OWNER_UID: user.uid,
            },
        )
        board = cast(Board, model)  # Type narrowing to keep static type checker happy.
        return board

    def get_board(self, uid: str) -> Board:
        """
        Retrieve a board from the database by its unique identifier (UID).

        Args:
            uid (str): The unique identifier of the board.

        Returns:
            Board: The Board object corresponding to the provided UID.

        Raises:
            `RecommendDBModelNotFound` if the user is not found.
        """
        model = self.__db.get(
            RecommendModelType.BOARD, {Key.RECOMMEND_MODEL_ATTR_UID: uid}
        )
        board = cast(Board, model)  # Type narrowing to keep static type checker happy.
        return board

    def get_board_by_name(self, name: str, user: User) -> Board:
        """
        Retrieve a board from the database by its name and the associated user.

        Args:
            name (str): The name of the board.
            user (User): The user who owns the board.

        Returns:
            Board: The Board object corresponding to the provided name and user.

        Raises:
            `RecommendDBModelNotFound` if the board is not found.
        """
        model = self.__db.get(
            RecommendModelType.BOARD,
            {
                Key.RECOMMEND_MODEL_ATTR_BOARD_NAME: name,
                Key.RECOMMEND_MODEL_ATTR_BOARD_OWNER_UID: user.uid,
            },
        )
        board = cast(Board, model)  # Type narrowing to keep static type checker happy.
        return board

    def get_all_boards(self, user: User) -> list[Board]:
        """
        Retrieve all boards associated with a specific user.

        Args:
            user (User): The user whose boards are to be retrieved.

        Returns:
            list[Board]: A list of Board objects belonging to the user.

        Raises:
            `RecommendDBModelNotFound` if the boards are not found.
        """
        models = self.__db.get_all(
            RecommendModelType.BOARD,
            {Key.RECOMMEND_MODEL_ATTR_BOARD_OWNER_UID: user.uid},
        )
        board = cast(
            list[Board], models
        )  # Type narrowing to keep static type checker happy.
        return board

    def remove_board(self, board: Board) -> bool:
        """
        Remove a board from the database.

        Args:
            board (Board): The Board object to be removed.

        Returns:
            bool: True if the board was successfully removed, False otherwise.
        """
        return self.__db.remove(board)

    ###########################################################################
    # Cards
    ###########################################################################
    def add_card(
        self, url: str, title: str, description: str, image: str, board: Board
    ) -> Card:
        """
        Add a new card to the database, associated with a specific board.

        Args:
            url (str): The URL associated with the card.
            title (str): The title of the card.
            description (str): A description of the card.
            image (str): The URL of the image associated with the card.
            board (Board): The board to which the card belongs.

        Returns:
            Card: The newly created Card object.

        Raises:
            `RecommendDBModelCreationError` if card creation fails.
        """
        model = self.__db.add(
            RecommendModelType.CARD,
            {
                Key.RECOMMEND_MODEL_ATTR_CARD_URL: url,
                Key.RECOMMEND_MODEL_ATTR_CARD_TITLE: title,
                Key.RECOMMEND_MODEL_ATTR_CARD_DESCRIPTION: description,
                Key.RECOMMEND_MODEL_ATTR_CARD_IMAGE: image,
                Key.RECOMMEND_MODEL_ATTR_CARD_BOARD_UID: board.uid,
            },
        )
        card = cast(Card, model)  # Type narrowing to keep static type checker happy.
        return card

    def get_card(self, uid: str) -> Card:
        """
        Retrieve a card from the database by its unique identifier (UID).

        Args:
            uid (str): The unique identifier of the card.

        Returns:
            Card: The Card object corresponding to the provided UID.

        Raises:
            `RecommendDBModelNotFound` if the user is not found.
        """
        model = self.__db.get(
            RecommendModelType.CARD, {Key.RECOMMEND_MODEL_ATTR_UID: uid}
        )
        card = cast(Card, model)  # Type narrowing to keep static type checker happy.
        return card

    def get_card_by_url(self, url: str, board: Board) -> Card:
        """
        Retrieve a card from the database by its URL and the associated board.

        Args:
            url (str): The URL associated with the card.
            board (Board): The board to which the card belongs.

        Returns:
            Card: The Card object corresponding to the provided URL and board.

        Raises:
            `RecommendDBModelNotFound` if the board is not found.
        """
        model = self.__db.get(
            RecommendModelType.CARD,
            {
                Key.RECOMMEND_MODEL_ATTR_CARD_URL: url,
                Key.RECOMMEND_MODEL_ATTR_CARD_BOARD_UID: board.uid,
            },
        )
        card = cast(Card, model)  # Type narrowing to keep static type checker happy.
        return card

    def get_all_cards(self, board: Board) -> list[Card]:
        """
        Retrieve all cards associated with a specific board.

        Args:
            board (Board): The board whose cards are to be retrieved.

        Returns:
            list[Card]: A list of Card objects belonging to the board.

        Raises:
            `RecommendDBModelNotFound` if the boards are not found.
        """
        models = self.__db.get_all(
            RecommendModelType.CARD,
            {Key.RECOMMEND_MODEL_ATTR_CARD_BOARD_UID: board.uid},
        )
        cards = cast(
            list[Card], models
        )  # Type narrowing to keep static type checker happy.
        return cards

    def remove_card(self, card: Card) -> bool:
        """
        Remove a card from the database.

        Args:
            card (Card): The Card object to be removed.

        Returns:
            bool: True if the card was successfully removed, False otherwise.
        """
        return self.__db.remove(card)
