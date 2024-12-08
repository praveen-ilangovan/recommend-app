"""
Get the card information from the URL
"""

# Local imports
from ..db.models.card import NewCard
from . import using_requests

# -----------------------------------------------------------------------------#
# Function
# -----------------------------------------------------------------------------#


def from_url(url: str) -> NewCard:
    """
    Extract the information a card holds from a URL

    Args:
        url (str): Url to be parsed

    Returns:
        NewCard

    Raises:
        RecommendAppError
    """
    data = using_requests.scrap(url)
    if not data.get("url"):
        data["url"] = url

    return NewCard(**data)
