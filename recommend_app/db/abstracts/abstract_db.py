"""
Module: db.abstracts.abstract_db
================================

This module defines the abstract base class `AbstractRecommendDB`, which
serves as a blueprint for database interaction within the recommend_app. Any
concrete database implementation must inherit from this class and implement the
required methods for connecting to the database, adding, retrieving, and
removing models such as users, boards, and cards.

This abstraction allows the application to remain database-agnostic and makes
it easier to switch between different database implementations without
modifying the core logic.
"""

# Builtin imports
from abc import ABC, abstractmethod


class AbstractRecommendDB(ABC):
    """
    Abstract base class for database interactions in the recommend_app.

    This class defines the contract that any concrete database implementation
    must fulfill. It includes methods for connecting to the database, adding
    models, retrieving single or multiple models, and removing models. The
    exact implementation details will vary depending on the specific database
    being used.
    """

    def __init__(self):
        """
        Initialize the AbstractRecommendDB class.

        This constructor is intended to be called by subclasses, ensuring
        proper initialization of the base class.
        """
        super().__init__()

    ###########################################################################
    # Methods: Abstracts
    ###########################################################################
    @abstractmethod
    async def connect(self) -> bool:
        """
        Establish a connection to the database.

        Returns:
            bool: True if the connection was successful, False otherwise.
        """
