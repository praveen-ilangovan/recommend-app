"""
Route to scrap the data from the URL
"""

# Project specific imports
from fastapi import APIRouter, status, HTTPException

# Local imports
from ...db.models.card import NewCard
from ...exceptions import RecommendAppError
from ... import scrapper

router = APIRouter()


# -----------------------------------------------------------------------------#
# Routes
# -----------------------------------------------------------------------------#
@router.get("/", status_code=status.HTTP_200_OK, response_model=NewCard)
async def scrap_url(url: str = "") -> NewCard:
    if not url:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Please provide an url to scrap"},
        )
    try:
        card = scrapper.from_url(url)
    except RecommendAppError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail={"error": err.message}
        )

    return card
