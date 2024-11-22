"""
Test user related models
"""

# Project specific imports
from pydantic_core import ValidationError
import pytest

# Local imports
from recommend_app.db.models.user import NewUser
from recommend_app.db.types import CrudType, RecommendModelType

#-----------------------------------------------------------------------------#
# Tests
#-----------------------------------------------------------------------------#
def test_new_user_model():
    new_user = NewUser(email_address="john.doe@mail.com",
                       user_name="john_doe",
                       first_name="John",
                       last_name="Doe",
                       password="password123")
    assert new_user.email_address == "john.doe@mail.com"
    assert new_user.crud_type == CrudType.CREATE
    assert new_user.model_type == RecommendModelType.USER

def test_new_user_model_with_invalid_email():
    with pytest.raises(ValidationError):
        new_user = NewUser(email_address="john.doe",
                        user_name="john_doe",
                        first_name="John",
                        last_name="Doe",
                        password="password123")
