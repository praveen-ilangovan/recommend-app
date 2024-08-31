"""
Module: card.py
===============

This module defines the `Card` model, which represents an individual
recommendation in the recommend_app. The `Card` model inherits from the
`AbstractRecommendModel` class, ensuring that it adheres to a consistent
structure with other models in the application. Each `Card` instance is
immutable and identified by a unique identifier (UID), along with additional
attributes such as a URL, title, description, image, and the UID of the board it belongs to.

The `Card` model is crucial for encapsulating recommendation details and
associating them with specific boards, allowing users to organize and share
their recommendations effectively.
"""

# Builtin imports
from dataclasses import dataclass, field

# Local imports
from ..abstracts.abstract_model import AbstractRecommendModel
from . import constants as Key


@dataclass(frozen=True, kw_only=True)
class Card(AbstractRecommendModel):
    """
    Model representing a recommendation card in the recommend_app.

    This class inherits from `AbstractRecommendModel` and represents a
    recommendation card with a unique identifier (UID), a URL, title,
    description, image, and the UID of the board to which the card belongs.
    The class is immutable (due to `frozen=True`), ensuring that instances
    cannot be modified after creation, which maintains data integrity.

    Attributes:
        url (str): The URL associated with the card.
        title (str): The title of the card.
        description (str): A description of the card. This field is optional
                           and not included in the string representation.
        image (str): An image URL associated with the card. This field is
                     optional and not included in the string representation.
        board_uid (str): The unique identifier of the board to which the card
                         belongs.
    """

    url: str
    title: str = field(compare=False)
    description: str = field(default="", repr=False, compare=False)
    image: str = field(default="", repr=False, compare=False)
    board_uid: str = field(default="", compare=True)

    ###########################################################################
    # Property
    ###########################################################################
    @property
    def type(self) -> str:
        """
        Returns the type of the model, which is 'Card'.

        This property overrides the abstract `type` property from the
        `AbstractRecommendModel` class.

        Returns:
            str: The string constant representing the type of the model, 'Card'.
        """
        return Key.RECOMMEND_MODEL_CARD

    ###########################################################################
    # Dunders
    ###########################################################################
    def __str__(self) -> str:
        """
        Returns a string representation of the Card instance.

        The string includes the model type ('Card') and the card's URL, title,
        and board UID, in the format: 'Card: [url, title, board_uid]'.

        Returns:
            str: A string representation of the Card instance.
        """
        return f"{self.type}: [{self.url}, {self.title}, {self.board_uid}]"
