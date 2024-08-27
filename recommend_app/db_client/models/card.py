"""
Module: card

This module defines the `Card` class, which represents a card-like structure
containing a URL, title, description, image, and a unique identifier (UID).
The `Card` class is implemented as an immutable data structure using Python's
`dataclass` decorator with the `frozen=True` option, making instances of this
class hashable and ensuring that they cannot be modified after creation.

Classes:
- Card: An immutable class representing a card with various attributes, such as
  a URL, title, description, image, and UID. It also includes a custom string
  representation for easier readability.

Attributes:
- url (str): The URL associated with the card.
- title (str): The title of the card. This field is excluded from comparisons.
- description (str): A brief description of the card. This field is excluded
  from both `repr` output and comparisons.
- image (str): The URL or path to the image associated with the card. This field
  is excluded from both `repr` output and comparisons.
- uid (str): A unique identifier for the card. This field is excluded from both
  `repr` output and comparisons.

Methods:
- __str__() -> str: Returns a string representation of the `Card` instance,
  displaying the card's title and URL.

Example usage:
    card = Card(url="https://example.com", title="Example Title")
    print(card)  # Output: Example Title [https://example.com]
"""

# Builtin imports
from dataclasses import dataclass, field

# Local imports
from ..abstracts.abstract_model import AbstractRecommendModel
from . import constants as Key


@dataclass(frozen=True, kw_only=True)
class Card(AbstractRecommendModel):
    """
    An immutable class representing a card with various attributes, such as
    a URL, title, description, image, and UID. It also includes a custom string
    representation for easier readability.

    Attributes:
        url (str): The URL associated with the card.
        title (str): The title of the card. This field is excluded from comparisons.
        description (str): A brief description of the card. This field is
                    excluded from both `repr` output and comparisons.
        image (str): The URL or path to the image associated with the card. This field
                    is excluded from both `repr` output and comparisons.
        uid (str): A unique identifier for the card. This field is excluded from both
                    `repr` output and comparisons.
    """

    url: str
    title: str = field(compare=False)
    description: str = field(default="", repr=False, compare=False)
    image: str = field(default="", repr=False, compare=False)
    uid: str = field(default="", repr=False, compare=False)

    ###########################################################################
    # Property
    ###########################################################################
    @property
    def type(self) -> str:
        """Return the type of this model"""
        return Key.RECOMMEND_MODEL_CARD

    ###########################################################################
    # Dunders
    ###########################################################################
    def __str__(self) -> str:
        """
        Returns a string representation of the `Card` instance, displaying the
        card's title and URL.
        """
        return f"{self.title} [{self.url}]"
