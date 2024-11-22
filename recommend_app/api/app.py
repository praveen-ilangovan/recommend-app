"""
FastAPI
"""

# Builtin imports
from contextlib import asynccontextmanager

# Project specific imports
from fastapi import FastAPI, status

# Local imports
from ..db import create_client
from . import dependencies

# -----------------------------------------------------------------------------#
# App
# -----------------------------------------------------------------------------#


# Lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Connect to the database
    client = create_client()
    await client.connect()
    print("Adding!!")
    dependencies.add_db_client(client)

    yield

    # Shutdown
    await client.disconnect()


app = FastAPI(lifespan=lifespan)

# -----------------------------------------------------------------------------#
# Routes
# -----------------------------------------------------------------------------#


@app.get("/health", tags=["Root"], status_code=status.HTTP_200_OK)
async def show_health() -> dict[str, str]:
    """
    Gives the health status of the connection
    """
    status = await dependencies.get_db_client().ping()
    return {"DB_Client": "active" if status else "inactive"}
