"""
Base Model. All the models should inherit from this class
"""

# Builtin imports
from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass(frozen=True, kw_only=True)
class AbstractRecommendModel(ABC):
    """
    AbstractRecommendModel stores the unique identifier of this entity

    Args:
        uid (str): A unique identifier for the user. Defaults to an empty string.
                The `uid` field is excluded from the `repr` output and from
                comparisons between `User` instances.
    """

    uid: str = field(default="", repr=False, compare=False)

    ###########################################################################
    # Property
    ###########################################################################
    @property
    @abstractmethod
    def type(self) -> str:
        """Return the type of this model"""
