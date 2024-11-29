"""
All the boards related routes

boards
    POST    /boards              - Add a new board to the db
"""

# Builtin imports
from typing import Any, cast, TYPE_CHECKING

# Project specific imports
from fastapi import APIRouter, status, HTTPException, Request

# Local imports
from ...db.models.board import NewBoard, BoardInDb
from ...db.exceptions import RecommendDBModelCreationError
from .. import auth, dependencies
from ... import ui

if TYPE_CHECKING:
    from ...db.models.user import UserInDb

router = APIRouter()


# -----------------------------------------------------------------------------#
# Routes
# -----------------------------------------------------------------------------#
@router.get("/new")
async def show_create_board_page(
    request: Request, user: auth.REQUIRED_USER
) -> ui.JinjaTemplateResponse:
    """
    Displays the page for users to create a new board
    """
    context: dict[str, Any] = {}
    if user:
        context["user"] = user
    return ui.show_page(request=request, name="boardForm.html", context=context)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=BoardInDb)
async def add_board(new_board: NewBoard, user: auth.REQUIRED_USER) -> BoardInDb:
    try:
        user = cast("UserInDb", user)  # Keeping MyPy happy.
        board = await dependencies.get_db_client().add_board(new_board, user)
    except RecommendDBModelCreationError as err:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail={"error": err.message})

    return board
