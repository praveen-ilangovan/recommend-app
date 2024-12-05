""" """

# Project specific imports
from pymongo import IndexModel

# Local imports
from .base import AbstractRecommendDocument
from ...models.card import FullCardAttributes, CardInDb


class CardDocument(FullCardAttributes, AbstractRecommendDocument):
    """
    Beanie ODM for users

    [ISSUE]: https://github.com/BeanieODM/beanie/issues/1036
    """

    # -------------------------------------------------------------------------#
    # Settings
    # -------------------------------------------------------------------------#
    class Settings:
        name = "cards"
        indexes = [IndexModel(["url", "board_id"], unique=True)]

    # -------------------------------------------------------------------------#
    # Properties
    # -------------------------------------------------------------------------#
    @property
    def recommend_inDb_model_type(self) -> type[CardInDb]:
        """
        Every document should map to its corresponding Recommend inDb model.
        They should be of type BaseRecommendModel
        """
        return CardInDb
