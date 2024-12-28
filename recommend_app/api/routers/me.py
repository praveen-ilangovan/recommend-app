"""
Landing page
"""

# Project specific imports
from fastapi import APIRouter, Request, status

# Local imports
from .. import auth, dependencies
from ..models import AuthUserWithBoards
from ... import ui


router = APIRouter()

# -----------------------------------------------------------------------------#
# Routes
# -----------------------------------------------------------------------------#


@router.get("/", status_code=status.HTTP_200_OK, response_model=AuthUserWithBoards)
async def show_landing_page(
    request: Request, user: auth.REQUIRED_USER, show_page: bool = True
) -> ui.JinjaTemplateResponse | AuthUserWithBoards:
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

    return AuthUserWithBoards(user=user, boards=boards)
