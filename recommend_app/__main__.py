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
    db = create_db()
    client = create_client(db)
    client.connect()

    user = client.add_user(str(time.time()))
    board1 = client.add_board("movies", user)

    result = client.remove_board(board1)
    print(result)


if __name__ == "__main__":
    main()
