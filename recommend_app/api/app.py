"""
FastAPI
"""

# Builtin imports
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING
import os

# Project specific imports
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv


# Local imports
from ..db import create_client
from .. import ui
from . import dependencies, exceptions
from .routers import session, users, boards, me, cards, scrapper, extension, internal


if TYPE_CHECKING:
    from ..db import RecommendDbClient


# Load the environment variables
load_dotenv()

# -----------------------------------------------------------------------------#
# App
# -----------------------------------------------------------------------------#


def get_db_client() -> "RecommendDbClient":
    """
    Create a db client and return it.

    Returns:
        `RecommendDbClient`
    """
    return create_client()


# Lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Connect to the database
    client = get_db_client()
    await client.connect()
    dependencies.add_db_client(client)

    yield

    # Shutdown
    await client.disconnect()


app = FastAPI(lifespan=lifespan)
app.include_router(users.router, tags=["Users"], prefix="/users")
app.include_router(session.router, tags=["Session"], prefix="/session")
app.include_router(boards.router, tags=["Boards"], prefix="/boards")
app.include_router(me.router, tags=["Me"], prefix="/me")
app.include_router(cards.router, tags=["Cards"], prefix="/cards")
app.include_router(scrapper.router, tags=["Scrapper"], prefix="/scrapper")
app.include_router(extension.router, tags=["Extension"], prefix="/extension")
app.include_router(internal.router, tags=["Internal"], prefix="/internal")


ui.mount_static_files(app)

# Middleware
origins = os.getenv("CORS_ORIGINS", [])
if origins:
    origins = origins.split(";")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------------------------------------------------#
# Routes
# -----------------------------------------------------------------------------#


@app.exception_handler(exceptions.RecommendAppRequiresLogin)
async def requires_login(request: Request, _: Exception):
    """
    Redirect the user to the login page
    """
    # return RedirectResponse(f"/session/new?next={quote(request.url._url)}")
    return RedirectResponse("/internal/session/new")
