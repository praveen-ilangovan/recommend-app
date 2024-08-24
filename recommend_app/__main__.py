"""
Entrypoint to the app
"""

# Project specific imports
from dotenv import load_dotenv

# Local imports
from .db.recommendDB import RecommendDB
from .db.models.user import User

# Load the environment variables
load_dotenv()


def main() -> None:
    """Main function"""

    db = RecommendDB.connect()

    user_id = db.add_user("test1219@example.com")
    user = db.get_user(user_id)
    res = db.remove_user(user)
    print(res)

    user = User("t@eple.com", _id="66c9fa30ead0ee3fdef76ad2")
    res = db.remove_user(user)
    print(res)


if __name__ == "__main__":
    main()
