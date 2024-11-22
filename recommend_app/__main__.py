"""
Entrypoint to the app
"""

# Builtin imports
import asyncio

# Project specific imports
from dotenv import load_dotenv

# Local imports
from . import db
from .db.models.user import NewUser

# Load the environment variables
load_dotenv()


async def main() -> None:
    """Main function"""
    print("Recommend App")

    client = db.create_client()
    await client.connect()

    new_user = NewUser(
        email_address="a7@email.com",
        user_name="117",
        first_name="fn",
        last_name="ln",
        password="teree",
    )

    result = await client.add_user(new_user)
    print(result)

    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
