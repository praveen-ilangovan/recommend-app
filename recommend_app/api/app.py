"""
FastAPI
"""

# Builtin imports
from contextlib import asynccontextmanager
import importlib.metadata
from typing import TYPE_CHECKING, Any
from urllib.parse import quote

# Project specific imports
from fastapi import FastAPI, status, Request
from fastapi.responses import RedirectResponse

# Local imports
from ..db import create_client
from ..db.exceptions import RecommendDBConnectionError
from .. import ui
from . import auth, dependencies, exceptions
from .routers import session, users, boards


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
app.include_router(boards.router, tags=["Boards"], prefix="/boards")

ui.mount_static_files(app)

# -----------------------------------------------------------------------------#
# Routes
# -----------------------------------------------------------------------------#


@app.exception_handler(exceptions.RecommendAppRequiresLogin)
async def requires_login(request: Request, _: Exception):
    """
    Redirect the user to the login page
    """
    return RedirectResponse(f"/session/new?next={quote(request.url._url)}")


@app.get("/health", tags=["Root"], status_code=status.HTTP_200_OK)
async def show_health(
    request: Request, user: auth.OPTIONAL_USER
) -> ui.JinjaTemplateResponse:
    """
    Gives the health status of the connection
    """
    try:
        status = await dependencies.get_db_client().ping()
    except RecommendDBConnectionError:
        status = None

    report = [
        {"key": "App Version", "value": importlib.metadata.version("recommend_app")},
        {"key": "DB Client", "value": "active" if status else "inactive"},
        {"key": "User", "value": "Authenticated" if user else "Unauthenticated"},
    ]

    context: dict[str, Any] = {"report": report}
    if user:
        context["user"] = user
    return ui.show_page(request=request, name="health.html", context=context)
