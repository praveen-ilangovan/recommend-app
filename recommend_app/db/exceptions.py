"""
Module: exceptions
==================

This module defines custom exceptions for handling specific errors related to
the recommend_app database. These exceptions inherit from the base
`RecommendAppError` class, which is used for application-level errors.
"""

# Local imports
from ..exceptions import RecommendAppError


class RecommendDBConnectionError(RecommendAppError):
    """
    Raised when a connection to the database fails. It indicates an issue with
    establishing or maintaining a database connection.
    """
