"""
A set of special endpoints for browser extension.

Browser extensions send the Authorization token in the request header.
"""

# Builtin imports
import json
from typing import Annotated
from datetime import timedelta

# Project specific imports
from fastapi import APIRouter, Request, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

# Local imports
from ...db.models.board import BoardInDb
from ...db.models.card import NewCard, CardInDb
from ...db.exceptions import (
    RecommendDBModelCreationError,
    RecommendDBModelNotFound,
    RecommendAppDbError,
)
from .. import auth, dependencies, constants

router = APIRouter()

# -----------------------------------------------------------------------------#
# Datamodel
# -----------------------------------------------------------------------------#


class AuthenticatedUserWithToken(auth.AuthenticatedUser):
    access_token: str


class AuthenticatedUserWithBoard(BaseModel):
    user: AuthenticatedUserWithToken
    boards: list[BoardInDb]


# -----------------------------------------------------------------------------#
# Functions
# -----------------------------------------------------------------------------#


def reissue_token(request: Request) -> AuthenticatedUserWithToken:
    """
    Grab the access token from the request header. Decode it and if it has
    expired, then use the user information available in the header to
    reissue a new token.

    Raises:
        HTTPException
    """
    data = request.headers.get("UserAuthData")
    if not data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Please sign in again."},
        )

    loaded_data = json.loads(data) or {}
    access_token = loaded_data.get("access_token", "")
    user = auth._decode_token(access_token)
    if not user:
        # Token has expired. Try refreshing this using the user data

        del loaded_data["access_token"]
        user = auth.AuthenticatedUser(**loaded_data)
        access_token_expires = timedelta(minutes=constants.ACCESS_TOKEN_EXPIRE_MINUTES)
        token = auth.create_access_token(user, access_token_expires)
        access_token = token.access_token

    return AuthenticatedUserWithToken(**user.model_dump(), access_token=access_token)


# -----------------------------------------------------------------------------#
# Routes
# -----------------------------------------------------------------------------#


@router.post(
    "/token", status_code=status.HTTP_200_OK, response_model=AuthenticatedUserWithToken
)
async def create_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> AuthenticatedUserWithToken:
    user = await auth.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Invalid signin credentials"},
        )

    access_token_expires = timedelta(minutes=constants.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = auth.create_access_token(user, access_token_expires)
    return AuthenticatedUserWithToken(
        **user.model_dump(), access_token=token.access_token
    )


@router.get(
    "/token", status_code=status.HTTP_200_OK, response_model=AuthenticatedUserWithBoard
)
async def get_verified_user(request: Request) -> AuthenticatedUserWithBoard:
    user = reissue_token(request=request)
    boards = await dependencies.get_db_client().get_all_boards(user.id)
    return AuthenticatedUserWithBoard(user=user, boards=boards)


@router.post("/{board_id}/cards", status_code=status.HTTP_201_CREATED)
async def add_card(request: Request, board_id: str, new_card: NewCard) -> CardInDb:
    reissue_token(request)

    try:
        card = await dependencies.get_db_client().add_card(new_card, board_id)
    except RecommendDBModelNotFound as err:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail={"error": err.message})
    except RecommendAppDbError as err:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail={"error": err.message})
    except RecommendDBModelCreationError as err:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail={"error": err.message})

    return card
