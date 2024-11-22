"""
Defines the dependencies
"""

# Builtin imports
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ..db.client import RecommendDbClient

# -----------------------------------------------------------------------------#
# Globals
# -----------------------------------------------------------------------------#
__DEPENDENCIES: dict[str, Any] = {}
DB_CLIENT = "db_client"

# -----------------------------------------------------------------------------#
# Functions
# -----------------------------------------------------------------------------#


def add(key: str, value: Any, force: bool = False) -> None:
    """
    Add a dependency to the dictionary

    Args:
        key (str): Name or the identifier for the dependency
        value (Any): Value of the dependency
        force (bool): If set to true, the value will be overwritten
    """
    if key not in __DEPENDENCIES or force:
        __DEPENDENCIES[key] = value


def get(key: str) -> Any:
    """
    Returns the value from the dictionary

    Args:
        key (str): Name or the identifier for the dependency

    Returns:
        Value if it exists, if not, None
    """
    return __DEPENDENCIES.get(key, None)


# -----------------------------------------------------------------------------#
# Utils
# -----------------------------------------------------------------------------#


def add_db_client(db_client: "RecommendDbClient") -> None:
    """
    Adds the instance of the db_client to the dependency dictionary

    Args:
        db_client (RecommendDbClient): Instance of the db client
    """
    add(DB_CLIENT, db_client)


def get_db_client() -> "RecommendDbClient":
    """
    Returns the instance of the db_client from the dependency dictionary

    Returns:
        Instance of the db client
    """
    return get(DB_CLIENT)
