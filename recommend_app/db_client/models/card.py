"""
Card: An item that can be recommended.

Card is the fundamental unit of this app. It stores the url of the item along
with some key metadata like a human readable name, a short description and an
image.
"""

# Builtin imports
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Card:
    """
    Dataclass that defines a card.

    Args:
        url (str): URL of an item
        title (str): Human readable name for this url
        description (str): A short description about what the url is about.
                           This is optional. Default is an empty string.
        image (str): Link to an image. Could be used as a thumbnail.
                     This is optional. Default is an empty string.
        uid (str): Id for this card. This is optional.
    """

    url: str
    title: str = field(compare=False)
    description: str = field(default="", repr=False, compare=False)
    image: str = field(default="", repr=False, compare=False)
    uid: str = field(default="", repr=False, compare=False)

    ###########################################################################
    # Dunders
    ###########################################################################
    def __str__(self) -> str:
        """Human readable representation of this instance."""
        return f"{self.title} [{self.url}]"
