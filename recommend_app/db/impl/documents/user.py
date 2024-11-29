""" """

# Builtin imports
from typing import Annotated, Optional

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

    # -------------------------------------------------------------------------#
    # Methods
    # -------------------------------------------------------------------------#
    @staticmethod
    async def get_document(attrs_dict: dict[str, str]) -> Optional["UserDocument"]:
        """
        Get the document from the db using the given attributes
        """
        keys = attrs_dict.keys()
        if "id" in keys:
            return await UserDocument.get(attrs_dict["id"])
        elif "email_address" in keys:
            return await UserDocument.find_one(
                UserDocument.email_address == attrs_dict["email_address"]
            )
        elif "user_name" in keys:
            return await UserDocument.find_one(
                UserDocument.user_name == attrs_dict["user_name"]
            )

        return None
