"""
Package: db.impl
================

This package implements the database interaction layer for the `recommend_app`
application using MongoDB and Beanie ODM

This package encapsulates all MongoDB-related logic, providing a cohesive and
modular approach to database management in the application.
"""

# Local imports
from .db import RecommendDB


def create_db(dbname: str) -> RecommendDB:
    """
    Create an instance of RecommendDB

    Args:
        dbname (str): Name of the database

    Returns:
        RecommendDB
    """
    return RecommendDB(dbname)
