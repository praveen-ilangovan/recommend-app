""" """

# Builtin imports
from typing import Annotated

# Project specific imports
from beanie import Indexed
from pydantic import EmailStr, field_validator

# Local imports
from .base import BaseRecommendDocument
from ...models.user import UserInDb
from ...hashing import Hasher


class UserDocument(BaseRecommendDocument):
    """
    Beanie ODM for users

    [ISSUE]: https://github.com/BeanieODM/beanie/issues/1036
    """

    # -------------------------------------------------------------------------#
    # Attributes
    # -------------------------------------------------------------------------#
    email_address: Annotated[EmailStr, Indexed(unique=True)]
    user_name: Annotated[str, Indexed(unique=True)]
    first_name: str
    last_name: str
    password: str

    @field_validator("password")
    def hash_password(cls, password: str) -> str:
        return Hasher.hash_password(password)

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
