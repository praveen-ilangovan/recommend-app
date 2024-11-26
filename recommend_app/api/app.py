"""
FastAPI
"""

# Builtin imports
from contextlib import asynccontextmanager
import importlib.metadata

# Project specific imports
from fastapi import FastAPI, status, Request, HTTPException

# Local imports
from ..db import create_client
from .. import ui
from . import dependencies
from .routers import session, users
from . import auth


# -----------------------------------------------------------------------------#
# App
# -----------------------------------------------------------------------------#


# Lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Connect to the database
    client = create_client()
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
    try:
        print(user)
    except HTTPException:
        print("No user")

    status = await dependencies.get_db_client().ping()
    report = [
        {"key": "App Version", "value": importlib.metadata.version("recommend_app")},
        {"key": "DB Client", "value": "active" if status else "inactive"},
    ]
    return ui.show_page(request=request, name="health.html", context={"report": report})
