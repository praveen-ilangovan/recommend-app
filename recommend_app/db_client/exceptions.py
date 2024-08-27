"""
Module: recommend_app.db_client.exceptions

This module defines custom exceptions for handling specific errors related to
the recommend_app database. These exceptions inherit from the base
`RecommendAppError` class, which is used for application-level errors.

Classes:
- RecommendDBConnectionError: Raised when a connection to the database
  fails. It indicates an issue with establishing or maintaining a database
  connection.

- RecommendDBModelCreationError: Raised when there is a failure in creating a
  new model (e.g., a user) in the database. This could occur due to
  constraints or other database errors during the creation process.

- RecommendDBModelNotFound: Raised when a requested model (e.g., a user) is not
  found in the database. This is useful for handling cases where queries for
  non-existent records are made.

Example usage:
    from recommend_app.db_client.exceptions import (
        RecommendDBConnectionError,
        RecommendDBModelCreationError,
        RecommendDBModelNotFound
    )

    try:
        db_client.connect()
    except RecommendDBConnectionError as e:
        # Handle connection failure
        print(f"Error: {e}")

    try:
        user = db_client.add_user("user@example.com")
    except RecommendDBModelCreationError as e:
        # Handle model creation failure
        print(f"Error: {e}")

    try:
        user = db_client.get_user("user@example.com")
    except RecommendDBModelNotFound as e:
        # Handle case where user is not found
        print(f"Error: {e}")

Dependencies:
- RecommendAppError: A base exception class from the `exceptions` module that
  all custom exceptions in the application inherit from.

These custom exceptions help differentiate between various error types,
allowing for more precise error handling in the app's database operations.
"""

# Local imports
from ..exceptions import RecommendAppError


class RecommendDBConnectionError(RecommendAppError):
    """
    Raised when a connection to the recommend_app database fails. It indicates
    an issue with establishing or maintaining a database connection.
    """


class RecommendDBModelCreationError(RecommendAppError):
    """
    Raised when there is a failure in creating a new model (e.g., a user) in
    the database. This could occur due to duplication or other database errors
    during the creation process.
    """


class RecommendDBModelNotFound(RecommendAppError):
    """
    Raised when a requested model (e.g., a user) is not found in the database.
    This is useful for handling cases where queries for non-existent records
    are made.
    """


class RecommendDBModelTypeError(RecommendAppError):
    """
    Raised when the method expects a model of a particular type but received
    something else.
    """
