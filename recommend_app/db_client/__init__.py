"""
Package: db_client

This package contains classes for database interactions within the
application. It provides a database client for managing connections, executing
queries, and performing CRUD operations. Additionally, it includes models
that define the structure of the database tables and relationships.

Modules:
- client.py: Contains the DatabaseClient class to handle database connections
             and queries.
- models/base.py : Contains the base model that represents the database tables.
- models/user.py : Inherits base model and represents a database user
- models/board.py : Inherits base model and represents a board and the
            relationship with the user.
"""

# Builtin imports
from typing import TYPE_CHECKING

# Local imports
from .client import RecommendDbClient

if TYPE_CHECKING:
    from .abstract_db import AbstractRecommendDB


def create_client(db: "AbstractRecommendDB") -> RecommendDbClient:
    """
    Create a client

    Args:
        db (AbstractRecommendDB): Child of this abstract class
    """
    return RecommendDbClient(db)
