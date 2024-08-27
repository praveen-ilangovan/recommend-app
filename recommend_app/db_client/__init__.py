"""
Package: recommend_app.db_client

This package provides the core components and utilities for interacting with the
application's database and data models. It includes the abstract base class for
defining the database interface, a client class for database interactions, and custom
exceptions for handling database-related errors.

Modules:
- client.py: Contains the `RecommendDbClient` class, which provides a
  higher-level interface for interacting with the database. This class
  manages common operations such as connecting to the database, adding,
  retrieving, and removing users, boards and cards.

- abstract_db.py: Defines the `AbstractRecommendDB` class, which serves as a
  blueprint for implementing database interactions. Any concrete database
  implementation must inherit from this class and implement its abstract methods.

- exceptions.py: Defines custom exceptions related to this subpackage.
  These include `RecommendDBConnectionError`, `RecommendDBModelCreationError`,
  and `RecommendDBModelNotFound`, which are used to handle specific error
  scenarios in database operations.

- models: Contains the data models used in the application, such as users
  and cards. These models are implemented using Python's `dataclass` decorator
  for simplicity and immutability.

  Modules:
  - user.py: Defines the `User` class, representing a user entity with an email
    address and unique identifier (UID).
  - card.py: Defines the `Card` class, an immutable data structure that represents
    a card entity containing details such as URL, title, description, image, and UID.


Usage:
    # Initialize the database client
    from recommend_app.db_client import create_client
    db_client = create_client(db=SomeRecommendDBImplementation())

    # Connect to the database
    db_client.connect()

    # Perform operations such as adding and retrieving users
    new_user = db_client.add_user("user@example.com")
    retrieved_user = db_client.get_user(new_user.id)

This package encapsulates both database operations and data modeling, providing
a unified interface to interact with the core components of the system.
It promotes modularity, flexibility, and robust error handling while ensuring
consistency in how data is represented and manipulated across the application.
"""

# Builtin imports
from typing import TYPE_CHECKING

# Local imports
from .client import RecommendDbClient

if TYPE_CHECKING:
    from .abstracts.abstract_db import AbstractRecommendDB


def create_client(db: "AbstractRecommendDB") -> RecommendDbClient:
    """
    Factory function to create and return an instance of `RecommendDbClient`.

    Args:
        db (AbstractRecommendDB): An instance of a class that implements the
        `AbstractRecommendDB` interface. This will be used by the
        `RecommendDbClient` to interact with the underlying database.

    Returns:
        RecommendDbClient: A client instance that interacts with the provided
        database implementation for performing operations such as connecting,
        adding, and retrieving users, boards and cards.

    Example usage:
        from recommend_app.db_client import create_client
        db_client = create_client(SomeRecommendDBImplementation())
        db_client.connect()
    """
    return RecommendDbClient(db)
