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
    request: Request, user: auth.REQUIRED_USER, show_page: bool = True
) -> ui.JinjaTemplateResponse:
    """
    Displays the landing page
    """
    boards = await dependencies.get_db_client().get_all_boards(user.id)

    if show_page:
        return ui.show_page(
            request=request,
            name="landing.html",
            context={"user": user, "boards": boards},
        )

    return boards
