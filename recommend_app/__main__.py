"""
Entrypoint to the app
"""

# Project specific imports
from dotenv import load_dotenv

# Local imports
from .db.recommendDB import RecommendDB

# Load the environment variables
load_dotenv()


def main() -> None:
    """Main function"""

    db = RecommendDB.connect()
    user_id = db.add_user("test1217@example.com")
    user = db.get_user(user_id)
    print(user)


if __name__ == "__main__":
    main()
