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
    print(user.uid)

    board = client.add_board("movies", user)
    print(board)

    user2 = client.add_user(str(time.time()))
    # print(user2.uid)

    board2 = client.add_board("movies", user2)

    board1 = client.get_board_by_name(board.name, user2)
    print(board1)

    print(board2 == board1)
    print(board == board1)

    # board = client.add_board("movies", user)
    # print(board)


if __name__ == "__main__":
    main()
