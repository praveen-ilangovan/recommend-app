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
    # result = await client.add_user(new_user)
    # print(result)

    email_address = "a@email.com"
    result = await client.get_user(email_address=email_address)
    print(result)

    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
