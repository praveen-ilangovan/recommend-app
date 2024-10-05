"""
Main entrypoint to the api
"""

# Builtin imports
from typing import TYPE_CHECKING

# Project specific imports
from fastapi import FastAPI

# Local imports
from ..db_client import create_client
from ..db_impl import create_db

from ..db_client.models.user import User

if TYPE_CHECKING:
    from ..db_client import RecommendDbClient

# ----------------------------------------------------------------------------#
# MONGO DB
# ----------------------------------------------------------------------------#
db = create_db()
client: "RecommendDbClient" = create_client(db)
client.connect()

# ----------------------------------------------------------------------------#
# FAST API APP
# ----------------------------------------------------------------------------#
app = FastAPI(
    title="Recommend APP",
    summary="A platform that allows users to organize and share their \
            favorite items across various categories, such as movies, books, \
            hotels, recipes, and more.",
)


# ----------------------------------------------------------------------------#
# Routes
# ----------------------------------------------------------------------------#
@app.get("/")
async def root():
    return {"message": "Recommend APP"}


# ----------------------------------------------------------------------------#
# Routes: Users
# ----------------------------------------------------------------------------#


@app.post("/api/v1/users/")
def add_user(user: User) -> User:
    """
    Add a new user.
    """
    new_user = client.add_user(user.email_address)
    return new_user
