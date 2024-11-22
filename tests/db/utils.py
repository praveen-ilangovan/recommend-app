# Builtin imports
import uuid

# Local imports
from recommend_app.db.models.user import NewUser

def get_random_name():
    return uuid.uuid4().hex

def create_user():
    user_name = get_random_name()
    return NewUser(email_address=f"{user_name}@mail.com",
                   user_name=user_name,
                   first_name="John",
                   last_name="Doe",
                   password="password123")
