"""
Landing page
"""

# Project specific imports
from fastapi import APIRouter, Request, status

# Local imports
from .. import auth, dependencies
from ..models import AuthUserWithBoards


router = APIRouter()

# -----------------------------------------------------------------------------#
# Routes
# -----------------------------------------------------------------------------#


@router.get("/", status_code=status.HTTP_200_OK, response_model=AuthUserWithBoards)
async def get_me(request: Request, user: auth.REQUIRED_USER) -> AuthUserWithBoards:
    """
    Get the logged in user data
    """
    boards = await dependencies.get_db_client().get_all_boards(user.id)
    return AuthUserWithBoards(user=user, boards=boards)
