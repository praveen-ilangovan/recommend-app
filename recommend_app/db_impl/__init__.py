"""
Package: db_impl
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
