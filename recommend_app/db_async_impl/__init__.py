# Local imports
from . import constants as Key
from .db import AsyncRecommendDB


def create_aysnc_db(dbname: str = Key.DB_NAME) -> AsyncRecommendDB:
    """
    Create an instance of RecommendDB

    Args:
        dbname (str): Name of the database

    Returns:
        RecommendDB
    """
    return AsyncRecommendDB(dbname)
