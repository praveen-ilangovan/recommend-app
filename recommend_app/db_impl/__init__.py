"""
Package: db_impl
================

This package implements the database interaction layer for the `recommend_app`
application using MongoDB.

Key Components:
---------------
1. **Sub-packages:**
    - `collections`: A sub-package that includes concrete implementations of
        MongoDB collections:
    - `Users`: Manages user-related documents with unique email addresses.
    - `Boards`: Manages board-related documents with unique compound indexes
        on board name and owner UID.
    - `Cards`: Manages card-related documents with unique compound indexes on
        card URL and board UID.

2. **Modules:**
    - `db.py`: Contains the `RecommendDB` class, which provides the main
    interface for connecting to and interacting with the MongoDB database. It
    handles operations such as adding, retrieving, and removing models, and
    initializes MongoDB collections.
    - `abstract_collection.py`: Defines the `AbstractCollection` class, an abstract
    base class for managing MongoDB collections. It provides methods for creating
    indexes, adding, finding, and removing documents, and handling the conversion
    between MongoDB documents and application models.

3. **Utilities:**
   - `create_db`: A function for creating an instance of `RecommendDB`,
     which provides methods for interacting with the database.

This package encapsulates all MongoDB-related logic, providing a cohesive and
modular approach to database management in the application.
"""

# Local imports
from . import constants as Key
from .db import RecommendDB


def create_db(dbname: str = Key.DB_NAME) -> RecommendDB:
    """
    Create an instance of RecommendDB

    Args:
        dbname (str): Name of the database

    Returns:
        RecommendDB
    """
    return RecommendDB(dbname)
