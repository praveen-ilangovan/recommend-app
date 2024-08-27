"""
Entrypoint to the app
"""

# Builtin imports
import time

# Project specific imports
from dotenv import load_dotenv

# Local imports
from .db_client import create_client
from .db_impl import create_db

# Load the environment variables
load_dotenv()


def main() -> None:
    """Main function"""
    # from .db_client.models import RecommendModelType
    # print(RecommendModelType('User'))

    db = create_db()
    client = create_client(db)
    client.connect()

    user = client.add_user(str(time.time()))
    print(user)
    client.remove_user(user)

    # user1 = client.get_user(user.uid)
    # print(user1.email_address)
    # # print(user == user1)


if __name__ == "__main__":
    main()
