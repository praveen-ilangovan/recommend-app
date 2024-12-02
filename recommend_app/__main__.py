"""
Entrypoint to the app
"""

# Builtin imports
import asyncio
import uuid

# Project specific imports
from dotenv import load_dotenv

# Local imports
from . import db
from .db.models.user import NewUser
from .db.models.board import NewBoard, UpdateBoard
from .db.hashing import Hasher
from .db.impl.documents.board import BoardDocument


# Load the environment variables
load_dotenv()


def get_random_name():
    return uuid.uuid4().hex


def create_user():
    user_name = get_random_name()
    return NewUser(
        email_address=f"{user_name}@mail.com",
        user_name=user_name,
        first_name="John",
        last_name="Doe",
        password="password123",
    )


async def main() -> None:
    """Main function"""
    print("Recommend App")

    client = db.create_client()
    await client.connect()

    # new_user = create_user()
    # pwd = new_user.password
    # result = await client.add_user(new_user)
    # print(result)

    # email_address = "praveen@email.com"
    # result = await client.get_user(email_address=email_address)
    # print(result)

    # boards = await BoardDocument.find({'owner_id': '6744a0ddee62a60d03f06d99', 'private':True}).to_list()
    # print(len(boards))

    # email_address = "praveen@email.com"
    # attrs_dict = {"email_address": email_address}
    # result = await UserDocument.find_one(attrs_dict)
    # print(result)

    # print(Hasher.verify_password(pwd, result.password))

    # new_board = NewBoard(name="Top Movies to Watch")
    # board = await client.add_board(new_board=new_board, owner=result)
    # print(board)

    # board_id = "67499a9c03cab482dce67296"
    # owner_id = "6744a0ddee62a60d03f06d99"

    # board = await client.get_board(board_id)
    # print(board)

    # board = await client.get_board(board_id, owner_id)
    # print(board)

    # board = await client.get_board("6749b1cbbe5aa922be16c31f", owner_id="1234")
    # print(board)


    # Update board
    data = UpdateBoard(private=True)
    await client.update_board("67499a5c8412707ee0bbef94", data)

    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
