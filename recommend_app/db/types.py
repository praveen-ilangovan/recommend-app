"""
Module: db.types
=================

Defines the enums: crud_type and model_type
"""

# Builtin imports
from enum import Enum

# Local imports
from . import constants as Key


# -----------------------------------------------------------------------------#
# Enums
# -----------------------------------------------------------------------------#
class RecommendModelType(Enum):
    """
    Enumeration for different types of models in the recommend_app.

    Attributes:
        USER: Represents the User model.
        BOARD: Represents the Board model.
        CARD: Represents the Card model.
    """

    USER = Key.RECOMMEND_MODEL_USER
    BOARD = Key.RECOMMEND_MODEL_BOARD
    CARD = Key.RECOMMEND_MODEL_CARD


class CrudType(Enum):
    """
    Enumeration for different crud operations.

    Attributes:
        CREATE: Type to represent a model that is used to create an object in DB
        READ: Type to represent a model that is used to read an object in DB
        UPDATE: Type to represent a model that is used to update an object in DB
    """

    CREATE = Key.RECOMMEND_MODEL_USER
    READ = Key.RECOMMEND_MODEL_BOARD
    UPDATE = Key.RECOMMEND_MODEL_CARD
