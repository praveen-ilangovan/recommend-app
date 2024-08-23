"""
recommend_app.db specific excpetions
"""


class RecommendDBDuplicateKeyError(BaseException):
    """
    Catches mongoDB's duplicate key error
    pymongo.errors.DuplicateKeyError: E11000 duplicate key error collection
    """
