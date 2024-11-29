""" """

# Builtin imports
from typing import Optional

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

    # -------------------------------------------------------------------------#
    # Methods
    # -------------------------------------------------------------------------#
    @staticmethod
    async def get_document(attrs_dict: dict[str, str]) -> Optional["BoardDocument"]:
        """
        Get the document from the db using the given attributes
        """
        keys = attrs_dict.keys()
        if "id" in keys:
            return await BoardDocument.get(attrs_dict["id"])

        # Extend it to return a list of board by its name or owner_id

        return None
