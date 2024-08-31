"""
sub-package: collections
========================

This sub-package defines the MongoDB collections used for managing different
types of recommendation data in the `recommend_app`.

Collections:
- `Users`: Handles operations related to user data, including indexing and
  retrieval.
- `Boards`: Manages board data, including setting up unique compound indexes
  for board names and owner UIDs.
- `Cards`: Manages card data, including enforcing uniqueness for card URLs
  within each board.

Each collection class inherits from `AbstractCollection` and implements
specific details for handling MongoDB documents associated with users, boards,
and cards.
"""

# Builtin imports
from typing import TypeAlias, Union

# Local imports
from .users import Users
from .boards import Boards
from .cards import Cards

Collection: TypeAlias = Union[Users, Boards, Cards]
