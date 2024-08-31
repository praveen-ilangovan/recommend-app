"""
Module: board.py
================

This module defines the `Board` model, which represents a collection of
recommendations (cards) grouped under a specific topic or name. The `Board`
model inherits from the `AbstractRecommendModel` class, ensuring that it
follows a consistent structure with other models in the recommend_app. Each
`Board` instance is immutable and identified by a unique identifier (UID),
a name, and the UID of its owner (a user).

The `Board` model is essential for organizing recommendations under specific
themes or categories, enabling users to share and manage their collections.
"""

# Builtin imports
from dataclasses import dataclass

# Local imports
from ..abstracts.abstract_model import AbstractRecommendModel
from . import constants as Key


@dataclass(frozen=True, kw_only=True)
class Board(AbstractRecommendModel):
    """
    Model representing a board in the recommend_app.

    This class inherits from `AbstractRecommendModel` and represents a board
    entity with a unique identifier (UID), a name, and the UID of the user who
    owns the board. Boards serve as containers for cards, which are individual
    recommendations. The class is immutable (due to `frozen=True`), ensuring
    data integrity by preventing modification after creation.

    Attributes:
        name (str): The name of the board.
        owner_uid (str): The unique identifier of the user who owns the board.
    """

    name: str
    owner_uid: str

    ###########################################################################
    # Property
    ###########################################################################
    @property
    def type(self) -> str:
        """
        Returns the type of the model, which is 'Board'.

        This property overrides the abstract `type` property from the
        `AbstractRecommendModel` class.

        Returns:
            str: The string constant representing the type of the model, 'Board'.
        """
        return Key.RECOMMEND_MODEL_BOARD

    ###########################################################################
    # Dunders
    ###########################################################################
    def __str__(self) -> str:
        """
        Returns a string representation of the Board instance.

        The string includes the model type ('Board') and the board's name along
        with its owner's UID, in the format: 'Board: [name, owner_uid]'.

        Returns:
            str: A string representation of the Board instance.
        """
        return f"{self.type}: [{self.name}, {self.owner_uid}]"
