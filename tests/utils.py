# Builtin imports
import uuid

# Local imports
from recommend_app.db.models.user import NewUser
from recommend_app.db.models.board import NewBoard
from recommend_app.api.auth import AuthenticatedUser

def get_random_name():
    return uuid.uuid4().hex

#-----------------------------------------------------------------------------#
# Factories
#-----------------------------------------------------------------------------#
def create_user():
    user_name = get_random_name()
    return NewUser(email_address=f"{user_name}@mail.com",
                   user_name=user_name,
                   first_name="John",
                   last_name="Doe",
                   password="password123")

def create_public_board():
    return NewBoard(name=get_random_name())

def create_private_board():
    return NewBoard(name=get_random_name(), private=True)

#-----------------------------------------------------------------------------#
# User overrides
#-----------------------------------------------------------------------------#
def get_fake_user():
    """
    Get a fake user
    """
    new_user = create_user()
    return AuthenticatedUser(sub=new_user.email_address,
                             email_address=new_user.email_address,
                             id='1234',
                             user_name=new_user.user_name,
                             first_name=new_user.first_name,
                             last_name=new_user.last_name)

def get_another_fake_user():
    """
    Get another fake user
    """
    new_user = create_user()
    return AuthenticatedUser(sub=new_user.email_address,
                             email_address=new_user.email_address,
                             id='2345',
                             user_name=new_user.user_name,
                             first_name=new_user.first_name,
                             last_name=new_user.last_name)

def get_no_user():
    return None
