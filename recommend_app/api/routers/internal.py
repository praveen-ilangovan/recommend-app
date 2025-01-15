"""
Internal routes to render jinja templates
"""

# Builtin imports
from typing import Any
import importlib.metadata

# Project specific imports
from fastapi import APIRouter, Request, status, HTTPException
from fastapi.responses import RedirectResponse

# Local imports
from .cards import get_board_and_card
from .. import auth, dependencies, constants
from ... import ui

from ...db.exceptions import (
    RecommendDBConnectionError,
    RecommendDBModelNotFound,
    RecommendAppDbError,
)

router = APIRouter()

# -----------------------------------------------------------------------------#
# Routes
# -----------------------------------------------------------------------------#


@router.get("/", status_code=status.HTTP_200_OK)
async def show_landing_page(
    request: Request, user: auth.REQUIRED_USER
) -> ui.JinjaTemplateResponse:
    """
    Displays the landing page
    """
    boards = await dependencies.get_db_client().get_all_boards(user.id)

    return ui.show_page(
        request=request,
        name="landing.html",
        context={"user": user, "boards": boards},
    )


@router.get("/health", tags=["Root"], status_code=status.HTTP_200_OK)
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


# -----------------------------------------------------------------------------#
# Routes - Register and Login
# -----------------------------------------------------------------------------#


@router.get("/users/new")
async def show_register_page(request: Request) -> ui.JinjaTemplateResponse:
    """
    Displays the register page for users to create a new account
    """
    return ui.show_page(request=request, name="register.html")


@router.get("/session/new")
async def show_login_page(request: Request) -> ui.JinjaTemplateResponse:
    """
    Show the login dialog to let the user log in.
    """
    return ui.show_page(request=request, name="login.html")


# -----------------------------------------------------------------------------#
# Routes - Users
# -----------------------------------------------------------------------------#


@router.get("/users/{requested_user_id}", status_code=status.HTTP_200_OK)
async def show_user_page(
    request: Request, requested_user_id: str, user: auth.OPTIONAL_USER
) -> ui.JinjaTemplateResponse:
    if user and requested_user_id == user.id:
        return RedirectResponse(constants.ROUTES.INTERNAL_LANDING)

    try:
        requested_user = await dependencies.get_db_client().get_user(requested_user_id)
        boards = await dependencies.get_db_client().get_all_boards(
            requested_user_id, only_public=True
        )
    except RecommendDBModelNotFound as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail={"error": err.message}
        )

    return ui.show_page(
        request=request,
        name="user.html",
        context={"user": user, "requested_user": requested_user, "boards": boards},
    )


# -----------------------------------------------------------------------------#
# Routes - Boards
# -----------------------------------------------------------------------------#


@router.get("/boards/new")
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


@router.get("/boards/{board_id}", status_code=status.HTTP_200_OK)
async def show_board(
    request: Request, board_id: str, user: auth.OPTIONAL_USER
) -> ui.JinjaTemplateResponse:
    try:
        owner_id = user.id if user else None
        board = await dependencies.get_db_client().get_board(board_id, owner_id)
        cards = await dependencies.get_db_client().get_all_cards(board_id)
    except RecommendDBModelNotFound as err:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail={"error": err.message})
    except RecommendAppDbError as err:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail={"error": err.message})

    return ui.show_page(
        request=request,
        name="board.html",
        context={"user": user, "board": board, "cards": cards},
    )


# -----------------------------------------------------------------------------#
# Routes - Cards
# -----------------------------------------------------------------------------#


@router.get("/boards/{board_id}/cards/new")
async def show_create_card_page(
    request: Request, board_id: str, user: auth.REQUIRED_USER
) -> ui.JinjaTemplateResponse:
    """
    Displays the page for users to create a new board
    """
    context = {"user": user, "board_id": board_id}
    return ui.show_page(request=request, name="cardForm.html", context=context)


@router.get("/cards/{card_id}", status_code=status.HTTP_200_OK)
async def show_card(
    request: Request, card_id: str, user: auth.OPTIONAL_USER
) -> ui.JinjaTemplateResponse:
    owner_id = user.id if user else None
    models = await get_board_and_card(card_id, owner_id)

    # If the board is private, only the owner can view it.
    if models.board.private and models.board.owner_id != owner_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Card belongs to a private board."},
        )

    return ui.show_page(
        request=request,
        name="card.html",
        context={"user": user, "board": models.board, "card": models.card},
    )
