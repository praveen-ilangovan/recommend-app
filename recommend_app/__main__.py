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

from .db_client.models.board import Board

# Load the environment variables
load_dotenv()


def main() -> None:
    """Main function"""
    db = create_db()
    client = create_client(db)
    client.connect()

    user = client.add_user(str(time.time()))
    print(user.uid)

    board = Board(name="movies", owner_uid="1234")
    print(board)

    board1 = Board(name="movies", owner_uid="1235")
    print(board1)

    print(board == board1)


if __name__ == "__main__":
    main()
