"""
Collections
"""

# Builtin imports
from typing import TypeAlias, Union

# Local imports
from .users import Users
from .boards import Boards

Collection: TypeAlias = Union[Users, Boards]
