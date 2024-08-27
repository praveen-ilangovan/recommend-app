"""
Board
"""

# Builtin imports
from dataclasses import dataclass

# Local imports
from ..abstracts.abstract_model import AbstractRecommendModel
from . import constants as Key


@dataclass(frozen=True, kw_only=True)
class Board(AbstractRecommendModel):
    """
    Represents a board. It has a name and also the user who created it.

    Args:
        name (str): Name of the board. This has to be unique for a user.
        owner_uid (str): Unique Identifier of the person who created it.
    """

    name: str
    owner_uid: str

    ###########################################################################
    # Property
    ###########################################################################
    @property
    def type(self) -> str:
        """Return the type of this model"""
        return Key.RECOMMEND_MODEL_BOARD

    ###########################################################################
    # Dunders
    ###########################################################################
    def __str__(self) -> str:
        """
        Returns a string representation of the `Board` instance, showing the
        board's name and the owner_id in a formatted way.
        """
        return f"Board: [name:{self.name}, owner_uid:{self.owner_uid}]"
