"""
FastAPI
"""

# Builtin imports
from contextlib import asynccontextmanager
import importlib.metadata
from typing import TYPE_CHECKING

# Project specific imports
from fastapi import FastAPI, status, Request

# Local imports
from ..db import create_client
from .. import ui
from . import dependencies
from .routers import session, users
from . import auth

if TYPE_CHECKING:
    from ..db import RecommendDbClient


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


ui.mount_static_files(app)

# -----------------------------------------------------------------------------#
# Routes
# -----------------------------------------------------------------------------#


@app.get("/health", tags=["Root"], status_code=status.HTTP_200_OK)
async def show_health(
    request: Request, user: auth.OPTIONAL_USER
) -> ui.JinjaTemplateResponse:
    """
    Gives the health status of the connection
    """
    status = await dependencies.get_db_client().ping()
    report = [
        {"key": "App Version", "value": importlib.metadata.version("recommend_app")},
        {"key": "DB Client", "value": "active" if status else "inactive"},
        {"key": "User", "value": "Authenticated" if user else "Unauthenticated"},
    ]

    context = {"report": report}
    if user:
        context["user"] = user
    return ui.show_page(request=request, name="health.html", context=context)
