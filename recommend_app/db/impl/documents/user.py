""" """

# Builtin imports
from typing import Annotated

# Project specific imports
from beanie import Indexed
from pydantic import EmailStr

# Local imports
from .base import AbstractRecommendDocument
from ...models.user import ExtendedUserAttributes, UserInDb


class UserDocument(ExtendedUserAttributes, AbstractRecommendDocument):
    """
    Beanie ODM for users

    [ISSUE]: https://github.com/BeanieODM/beanie/issues/1036
    """

    # -------------------------------------------------------------------------#
    # Attributes
    # -------------------------------------------------------------------------#
    email_address: Annotated[EmailStr, Indexed(unique=True)]
    user_name: Annotated[str, Indexed(unique=True)]

    # -------------------------------------------------------------------------#
    # Settings
    # -------------------------------------------------------------------------#
    class Settings:
        name = "users"

    # -------------------------------------------------------------------------#
    # Properties
    # -------------------------------------------------------------------------#
    @property
    def recommend_inDb_model_type(self) -> type[UserInDb]:
        """
        Every document should map to its corresponding Recommend inDb model.
        They should be of type BaseRecommendModel
        """
        return UserInDb
