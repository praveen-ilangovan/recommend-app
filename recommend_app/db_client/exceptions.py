"""
recommend_app.db specific excpetions
"""

# Local imports
from ..exceptions import RecommendAppError


class RecommendDBConnectionError(RecommendAppError):
    """
    Catches the db connection error
    """


class RecommendDBModelCreationError(RecommendAppError):
    """
    Thrown when adding a new object to db fails
    """


class RecommendDBModelNotFound(RecommendAppError):
    """
    Thrown if unable to get the object from the db
    """
