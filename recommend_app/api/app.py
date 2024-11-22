"""
FastAPI
"""

# Builtin imports
from contextlib import asynccontextmanager
import importlib.metadata

# Project specific imports
from fastapi import FastAPI, status, Request

# Local imports
from ..db import create_client
from .. import ui
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
    dependencies.add_db_client(client)

    yield

    # Shutdown
    await client.disconnect()


app = FastAPI(lifespan=lifespan)
ui.mount_static_files(app)

# -----------------------------------------------------------------------------#
# Routes
# -----------------------------------------------------------------------------#


@app.get("/health", tags=["Root"], status_code=status.HTTP_200_OK)
async def show_health(request: Request) -> ui.JinjaTemplateResponse:
    """
    Gives the health status of the connection
    """
    status = await dependencies.get_db_client().ping()
    report = [
        {"key": "App Version", "value": importlib.metadata.version("recommend_app")},
        {"key": "DB Client", "value": "active" if status else "inactive"},
    ]
    return ui.show_page(request=request, name="health.html", context={"report": report})
