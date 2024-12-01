"""
Module:db.models.bases
=======================

Defines the base models. One for each crud operation types.
"""

# Local imports
from ..abstracts.abstract_model import AbstractRecommendModel
from ..types import CrudType

# -----------------------------------------------------------------------------#
# Bases
# -----------------------------------------------------------------------------#


class BaseNewRecommendModel(AbstractRecommendModel):
    """
    Represents the model used to create a new entry in the database.
    """

    ###########################################################################
    # Properties
    ###########################################################################
    @property
    def crud_type(self) -> CrudType:
        """
        Returns the crud_type

        Returns:
            CrudType: Crud operation to be performed.
        """
        return CrudType.CREATE


class BaseRecommendModel(AbstractRecommendModel):
    """
    Represents the model used to get an entry from the database.

    Args:
        id (str|int): Uniqye id of this model in the DB
    """

    id: str

    ###########################################################################
    # Properties
    ###########################################################################
    @property
    def crud_type(self) -> CrudType:
        """
        Returns the crud_type

        Returns:
            CrudType: Crud operation to be performed.
        """
        return CrudType.READ
