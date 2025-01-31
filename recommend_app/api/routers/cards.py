"""
Get, Update and Remove card!!
"""

# Builtin imports
from typing import Optional

# Project specific imports
from fastapi import APIRouter, status, HTTPException, Request

# Local imports
from ...db.exceptions import RecommendDBModelNotFound, RecommendAppDbError
from ...db.models.card import UpdateCard
from .. import auth, dependencies
from ..models import BoardAndCard

router = APIRouter()

# -----------------------------------------------------------------------------#
# Function
# -----------------------------------------------------------------------------#


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
        if not user_id:
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED, detail={"error": err.message}
            )
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail={"error": err.message})

    return BoardAndCard(board=board, card=card)


# -----------------------------------------------------------------------------#
# Routes
# -----------------------------------------------------------------------------#
@router.get("/{card_id}", status_code=status.HTTP_200_OK, response_model=BoardAndCard)
async def get_card(
    request: Request, card_id: str, user: auth.OPTIONAL_USER
) -> BoardAndCard:
    owner_id = user.id if user else None
    model = await get_board_and_card(card_id, owner_id)

    # If the board is private, only the owner can view it.
    if model.board.private and model.board.owner_id != owner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"error": "Card belongs to a private board."},
        )

    return model


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
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"error": "Only owner can edit it."},
        )

    try:
        await dependencies.get_db_client().update_card(card_id, data)
    except RecommendDBModelNotFound as err:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail={"error": err.message})
    except RecommendAppDbError as err:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail={"error": err.message})


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
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"error": "Only owner can remove it."},
        )

    try:
        await dependencies.get_db_client().remove_card(card_id)
    except RecommendDBModelNotFound as err:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail={"error": err.message})
    except RecommendAppDbError as err:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail={"error": err.message})
