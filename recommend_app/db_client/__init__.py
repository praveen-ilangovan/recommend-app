"""
Package: db_client
===================

The `db_client` package provides the core functionality for interacting with
the database within the recommend_app. It defines the interface for database
operations, the data models used in the application, and utilities for creating
and managing these models. This package is central to the application's data
management and persistence layer.

Key Components:
---------------
1. **Sub-packages:**
   - `abstracts`: Contains abstract base classes that define the structure and
      behavior of the database and models.
     - `abstract_db.py`: Defines the abstract base class `AbstractRecommendDB`
       for database operations, outlining essential methods for connecting,
       adding, retrieving, and removing data.
     - `abstract_model.py`: Defines the abstract base class
       `AbstractRecommendModel` for data models, ensuring a consistent
       structure for all models.

   - `models`: Defines the core data models used in the application,
     inheriting from `AbstractRecommendModel`.
     - `user.py`: Contains the `User` model, representing users in the application.
     - `board.py`: Contains the `Board` model, representing boards that group recommendations.
     - `card.py`: Contains the `Card` model, representing individual recommendations.
     - `constants.py`: Defines constants used across the models to ensure consistency.

2. **Utilities:**
   - `create_model`: A factory function for creating instances of the
     `User`, `Board`, or `Card` models based on the specified type and attributes.
   - `create_client`: A function for creating an instance of `RecommendDbClient`,
     which provides methods for interacting with the database.

3. **Exceptions:**
   - `RecommendDBConnectionError`: Raised when there is a failure in connecting
     to the database.

Usage:
    # Initialize the database client
    from recommend_app.db_client import create_client
    db_client = create_client(db=SomeRecommendDBImplementation())

    # Connect to the database
    db_client.connect()

    # Perform operations
    new_user = db_client.add_user("user@example.com")
    movies_board = client.add_board("movies", new_user)
    card = client.add_card(url, title, description, image, board=movies_board)

This package ensures a cohesive approach to managing and interacting with the
application's data, providing a consistent interface for different database
backends and maintaining a clean architecture for data models and operations.
"""

# Builtin imports
from typing import TYPE_CHECKING

# Local imports
from .client import RecommendDbClient

if TYPE_CHECKING:
    from .abstracts.abstract_db import AbstractRecommendDB


def create_client(db: "AbstractRecommendDB") -> RecommendDbClient:
    """
    Factory function to create an instance of `RecommendDbClient`.

    Args:
        db (AbstractRecommendDB): An instance of a class implementing the
                                 `AbstractRecommendDB` interface, which
                                  defines the database operations.

    Returns:
        RecommendDbClient: An instance of `RecommendDbClient`
        initialized with the provided database instance.
    """
    return RecommendDbClient(db)
