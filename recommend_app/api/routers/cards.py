"""
Get, Update and Remove card!!
"""

# Builtin imports
from typing import Union

# Project specific imports
from fastapi import APIRouter, status, HTTPException, Request

# Local imports
from ... import ui
from ...db.exceptions import RecommendDBModelNotFound, RecommendAppDbError
from ...db.models.card import CardInDb
from .. import auth, dependencies


router = APIRouter()


# -----------------------------------------------------------------------------#
# Routes
# -----------------------------------------------------------------------------#
@router.get("/{card_id}", status_code=status.HTTP_200_OK, response_model=CardInDb)
async def get_card(
    request: Request, card_id: str, user: auth.OPTIONAL_USER, show_page: bool = True
) -> Union[ui.JinjaTemplateResponse, CardInDb]:
    owner_id = user.id if user else None
    try:
        card = await dependencies.get_db_client().get_card(card_id)
        board = await dependencies.get_db_client().get_board(card.board_id, owner_id)
        if board.owner_id != owner_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"error": "Card belongs to a private board."},
            )

    except RecommendDBModelNotFound as err:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail={"error": err.message})
    except RecommendAppDbError as err:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail={"error": err.message})

    if show_page:
        return ui.show_page(
            request=request,
            name="card.html",
            context={"user": user, "board": board, "card": card},
        )
    return card
