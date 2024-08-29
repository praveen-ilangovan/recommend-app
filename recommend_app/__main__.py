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


"""
TODO
[] Rename models constants *_ID to *_UID
[] Card.title or Card.name?? (Board has a name and not title.)
[] Compare:
    User - EmailAddress
    Board - Name + OwnerUID
    Card - URL + BoardUID
"""

CARD_DATA = {
    "url": "https://www.netflix.com/gb/title/81767635",
    "title": "Godzilla minus one",
    "description": "In postwar Japan, a traumatized former fighter \
                            pilot joins the civilian effort to fight off a \
                            massive nuclear-enhanced monster attacking their \
                            shores.",
    "image": "url/to/the/image",
}


def main() -> None:
    """Main function"""
    db = create_db()
    client = create_client(db)
    client.connect()

    user = client.add_user(str(time.time()))
    board1 = client.add_board("movies", user)
    card = client.add_card(**CARD_DATA, board=board1)
    print(card)


if __name__ == "__main__":
    main()
