"""
Landing page
"""

# Project specific imports
from fastapi import APIRouter, Request

# Local imports
from .. import auth, dependencies
from ... import ui

router = APIRouter()

# -----------------------------------------------------------------------------#
# Routes
# -----------------------------------------------------------------------------#


@router.get("/")
async def show_landing_page(
    request: Request, user: auth.REQUIRED_USER
) -> ui.JinjaTemplateResponse:
    """
    Displays the landing page
    """
    boards = await dependencies.get_db_client().get_all_boards(user.id)
    return ui.show_page(
        request=request, name="landing.html", context={"user": user, "boards": boards}
    )
