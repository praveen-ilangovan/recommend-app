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
from ...db.models.board import NewBoard, BoardInDb, UpdateBoard
from ...db.models.card import NewCard, CardInDb

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


@router.put("/{board_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_board(board_id: str, data: UpdateBoard, user: auth.REQUIRED_USER):
    try:
        if not user:
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED,
                detail={"error": "Please sign in"},
            )

        board = await dependencies.get_db_client().get_board(board_id, user.id)

        # Only the owners of the board can update it
        if board.owner_id != user.id:
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED,
                detail={"error": "Only owners can update the board"},
            )

        await dependencies.get_db_client().update_board(board.id, data)
    except RecommendDBModelNotFound as err:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail={"error": err.message})
    except RecommendAppDbError as err:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail={"error": err.message})


@router.delete("/{board_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_board(board_id: str, user: auth.REQUIRED_USER):
    try:
        if not user:
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED,
                detail={"error": "Please sign in"},
            )

        board = await dependencies.get_db_client().get_board(board_id, user.id)

        # Only the owners of the board can delete it
        if board.owner_id != user.id:
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED,
                detail={"error": "Only owners can delete the board"},
            )

        await dependencies.get_db_client().remove_board(board.id)
    except RecommendDBModelNotFound as err:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail={"error": err.message})
    except RecommendAppDbError as err:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail={"error": err.message})


# -----------------------------------------------------------------------------#
# Routes: Cards
# -----------------------------------------------------------------------------#


@router.post(
    "/{board_id}/cards", status_code=status.HTTP_201_CREATED, response_model=CardInDb
)
async def add_card(
    board_id: str, new_card: NewCard, user: auth.REQUIRED_USER
) -> CardInDb:
    if not user:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, detail={"error": "Invalid user: None"}
        )

    try:
        # Make sure the board belongs to the user
        board = await dependencies.get_db_client().get_board(board_id, user.id)
        if board.owner_id != user.id:
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED,
                detail={"error": "Only owner can add a card to the board."},
            )

        card = await dependencies.get_db_client().add_card(new_card, board_id)

    except RecommendDBModelNotFound as err:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail={"error": err.message})
    except RecommendAppDbError as err:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail={"error": err.message})
    except RecommendDBModelCreationError as err:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail={"error": err.message})

    return card
