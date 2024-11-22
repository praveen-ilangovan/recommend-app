"""
Base Document
"""

# Builtin imports
from typing import TYPE_CHECKING, cast
from abc import ABC, abstractmethod

# Project specific imports
from beanie import Document

if TYPE_CHECKING:
    from ...models.bases import BaseRecommendModel
    from ...abstracts.abstract_model import AbstractRecommendModel


class BaseRecommendDocument(ABC, Document):
    """
    Base document class
    """

    # -------------------------------------------------------------------------#
    # Abstracts
    # -------------------------------------------------------------------------#
    @property
    @abstractmethod
    def recommend_inDb_model_type(self) -> type["BaseRecommendModel"]:
        """
        Every document should map to its corresponding Recommend inDb model.
        They should be of type BaseRecommendModel
        """

    # -------------------------------------------------------------------------#
    # Class Method
    # -------------------------------------------------------------------------#
    @classmethod
    def from_model(cls, model: "AbstractRecommendModel") -> "BaseRecommendDocument":
        """
        Create an instance of the Beanie Document from the RecommendModel.
        RecommendModel to RecommendDocument
        """
        return cls(**model.model_dump())

    # -------------------------------------------------------------------------#
    # Methods
    # -------------------------------------------------------------------------#
    def to_model(self) -> "BaseRecommendModel":
        """
        RecommendDocument to RecommendModel
        """
        return_dict = {}
        for key, value in self.model_dump().items():
            if key == "id":
                return_dict["id"] = str(value)
            elif key == "revision_id":
                continue
            else:
                return_dict[key] = value

        return cast("BaseRecommendModel", self.recommend_inDb_model_type(**return_dict))
