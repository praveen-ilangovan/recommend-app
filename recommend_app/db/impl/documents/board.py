""" """

# Local imports
from .base import AbstractRecommendDocument
from ...models.board import ExtendedBoardAttributes, BoardInDb


class BoardDocument(ExtendedBoardAttributes, AbstractRecommendDocument):
    """
    Beanie ODM for boards
    """

    # -------------------------------------------------------------------------#
    # Settings
    # -------------------------------------------------------------------------#
    class Settings:
        name = "boards"

    # -------------------------------------------------------------------------#
    # Properties
    # -------------------------------------------------------------------------#
    @property
    def recommend_inDb_model_type(self) -> type[BoardInDb]:
        """
        Every document should map to its corresponding Recommend inDb model.
        They should be of type BaseRecommendModel
        """
        return BoardInDb
