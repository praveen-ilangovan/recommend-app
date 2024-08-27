"""
Collection that holds all the users documents
"""

# Builtin imports
from typing import TYPE_CHECKING

# Local imports
from ..abstract_collection import AbstractCollection
from .. import constants as Key
from ...db_client.models import RecommendModelType

if TYPE_CHECKING:
    from pymongo.database import Database as MongoDB


class Users(AbstractCollection):
    def __init__(self, db: "MongoDB"):
        super().__init__(db)

        # Make email address a unique key
        self.create_index(Key.USER_EMAIL_ADDRESS, unique=True)

    ###########################################################################
    # Properties
    ###########################################################################
    @property
    def collection_name(self) -> str:
        """Returs the name of this collection"""
        return Key.COL_USERS

    @property
    def model_type(self) -> RecommendModelType:
        """Returns the name of the model type this class handles"""
        return RecommendModelType.USER
