"""
Entrypoint to the app
"""

# Builtin imports
import asyncio

# Project specific imports
from dotenv import load_dotenv

# Local imports
from . import db

# Load the environment variables
load_dotenv()


async def main() -> None:
    """Main function"""
    print("Recommend App")

    client = db.create_client()
    await client.connect()
    status = await client.ping()
    print(status)
    status = await client.disconnect()
    print(status)


if __name__ == "__main__":
    asyncio.run(main())
