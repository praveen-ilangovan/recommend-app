"""
Defines the user model
"""

# Builtin imports
from dataclasses import dataclass, field


@dataclass
class User:
    """
    Dataclass that defines a user.

    Args:
        email_address (str): Email address of the user
        uid (str): Id for this card. This is optional.
    """

    email_address: str
    _id: str = field(default="", repr=False, compare=False)

    ###########################################################################
    # Dunders
    ###########################################################################
    def __str__(self) -> str:
        """Human readable representation of this instance."""
        return f"User[{self.email_address}]"
