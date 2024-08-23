"""
recommend_app.db specific excpetions
"""


class RecommendDBConnectionError(BaseException):
    """
    Catches all the possible errors that could happen when the mongodb
    connection fails.

    Invalid URI -> pymongo.errors.InvalidURI
    Authentication failed -> pymongo.errors.OperationFailure
    Timeout error -> pymongo.errors.ServerSelectionTimeoutError
    """


class RecommendDBDuplicateKeyError(BaseException):
    """
    Catches mongoDB's duplicate key error
    pymongo.errors.DuplicateKeyError: E11000 duplicate key error collection
    """
