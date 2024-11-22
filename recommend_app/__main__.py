"""
Entrypoint to the app
"""

# Builtin imports
import asyncio

# Project specific imports
from dotenv import load_dotenv

# Local imports
# from . import db
from .db.models.user import NewUser

# Load the environment variables
load_dotenv()


async def main() -> None:
    """Main function"""
    print("Recommend App")

    # client = db.create_client()
    # await client.connect()
    # status = await client.ping()
    # print(status)
    # status = await client.disconnect()
    # print(status)

    new_user = NewUser(
        email_address="a@email.com",
        user_name="11",
        first_name="fn",
        last_name="ln",
        password="teree",
    )
    print(new_user)
    print(new_user.type, new_user.crud_type, new_user.model_type)


if __name__ == "__main__":
    asyncio.run(main())
