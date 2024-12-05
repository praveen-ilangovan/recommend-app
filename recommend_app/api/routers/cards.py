"""
Get, Update and Remove card!!
"""

# Builtin imports
from typing import Union, Optional

# Project specific imports
from fastapi import APIRouter, status, HTTPException, Request
from pydantic import BaseModel

# Local imports
from ... import ui
from ...db.exceptions import RecommendDBModelNotFound, RecommendAppDbError
from ...db.models.board import BoardInDb
from ...db.models.card import CardInDb, UpdateCard
from .. import auth, dependencies

router = APIRouter()

# -----------------------------------------------------------------------------#
# Function
# -----------------------------------------------------------------------------#


class BoardAndCard(BaseModel):
    board: BoardInDb
    card: CardInDb


async def get_board_and_card(card_id: str, user_id: Optional[str]) -> BoardAndCard:
    """
    Get the card and its board from its ID

    Args:
        card_id (str): ID of the card to be edited
        user_id (str): ID of the signed in user. Optional
            Private boards could only be accessed by its owner.

    Returns:
        A dict of card and board.

    Raises:
        HTTPException
    """
    try:
        card = await dependencies.get_db_client().get_card(card_id)
        board = await dependencies.get_db_client().get_board(card.board_id, user_id)
    except RecommendDBModelNotFound as err:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail={"error": err.message})
    except RecommendAppDbError as err:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail={"error": err.message})

    return BoardAndCard(board=board, card=card)


# -----------------------------------------------------------------------------#
# Routes
# -----------------------------------------------------------------------------#
@router.get("/{card_id}", status_code=status.HTTP_200_OK, response_model=CardInDb)
async def get_card(
    request: Request, card_id: str, user: auth.OPTIONAL_USER, show_page: bool = True
) -> Union[ui.JinjaTemplateResponse, CardInDb]:
    owner_id = user.id if user else None
    models = await get_board_and_card(card_id, owner_id)

    # If the board is private, only the owner can view it.
    if models.board.private and models.board.owner_id != owner_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Card belongs to a private board."},
        )

    if show_page:
        return ui.show_page(
            request=request,
            name="card.html",
            context={"user": user, "board": models.board, "card": models.card},
        )
    return models.card


@router.put("/{card_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_card(card_id: str, data: UpdateCard, user: auth.REQUIRED_USER):
    if not user:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, detail={"error": "Please sign in"}
        )

    # Validate that the user is authorized to update this card
    models = await get_board_and_card(card_id, user.id)

    # Only the owner can edit it.
    if models.board.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Only owner can edit it."},
        )

    try:
        await dependencies.get_db_client().update_card(card_id, data)
    except RecommendDBModelNotFound as err:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail={"error": err.message})
    except RecommendAppDbError as err:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail={"error": err.message})


@router.delete("/{card_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_card(card_id: str, user: auth.REQUIRED_USER):
    if not user:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, detail={"error": "Please sign in"}
        )

    # Validate that the user is authorized to remove this card
    models = await get_board_and_card(card_id, user.id)

    # Only the owner can edit it.
    if models.board.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Only owner can remove it."},
        )

    try:
        await dependencies.get_db_client().remove_card(card_id)
    except RecommendDBModelNotFound as err:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail={"error": err.message})
    except RecommendAppDbError as err:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail={"error": err.message})
