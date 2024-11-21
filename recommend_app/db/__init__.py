"""
Package: db
===================

The `db` package provides the core functionality for interacting with
the database within the recommend_app. It defines the interface for database
operations, the data models used in the application, and utilities for creating
and managing these models. This package is central to the application's data
management and persistence layer.

Usage:
    # Initialize the database client
    from recommend_app.db_client import create_client
    db_client = create_client(db=SomeRecommendDBImplementation())

    # Connect to the database
    db_client.connect()

This package ensures a cohesive approach to managing and interacting with the
application's data, providing a consistent interface for different database
backends and maintaining a clean architecture for data models and operations.
"""

# Builtin imports
import os
from typing import TYPE_CHECKING, Optional

# Local imports
from .client import RecommendDbClient
from .impl.db import RecommendDB
from . import constants as Key

if TYPE_CHECKING:
    from .abstracts.abstract_db import AbstractRecommendDB


def create_client(db: Optional["AbstractRecommendDB"] = None) -> RecommendDbClient:
    """
    Factory function to create an instance of `RecommendDbClient`.

    Args:
        db (AbstractRecommendDB): An instance of a class implementing the
                                 `AbstractRecommendDB` interface, which
                                  defines the database operations. This is Optional.

    Returns:
        RecommendDbClient: An instance of `RecommendDbClient`
        initialized with the provided database instance.
    """
    db = db or RecommendDB(os.getenv("DB_NAME", Key.DB_NAME))
    return RecommendDbClient(db)
