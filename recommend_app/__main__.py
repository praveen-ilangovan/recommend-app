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
    print(db)
    # user_id = db.add_user("test121@example.com")
    # print(user_id)


if __name__ == "__main__":
    main()
