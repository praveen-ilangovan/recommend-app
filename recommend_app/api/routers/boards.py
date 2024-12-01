"""
All the boards related routes

boards
    POST    /boards              - Add a new board to the db
"""

# Builtin imports
from typing import Any

# Project specific imports
from fastapi import APIRouter, status, HTTPException, Request

# Local imports
from ...db.models.board import NewBoard, BoardInDb
from ...db.exceptions import (
    RecommendDBModelCreationError,
    RecommendDBModelNotFound,
    RecommendAppDbError,
)
from .. import auth, dependencies
from ... import ui

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
    if not user:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, detail={"error": "Invalid user: None"}
        )

    try:
        board = await dependencies.get_db_client().add_board(new_board, user.id)
    except RecommendDBModelCreationError as err:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail={"error": err.message})

    return board


@router.get("/{board_id}", status_code=status.HTTP_200_OK, response_model=BoardInDb)
async def get_board(board_id: str, user: auth.OPTIONAL_USER) -> BoardInDb:
    try:
        owner_id = user.id if user else None
        board = await dependencies.get_db_client().get_board(board_id, owner_id)
    except RecommendDBModelNotFound as err:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail={"error": err.message})
    except RecommendAppDbError as err:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail={"error": err.message})

    return board
