"""
A set of special endpoints for browser extension.

Browser extensions send the Authorization token in the request header.
"""

# Builtin imports
from typing import Annotated
from datetime import timedelta

# Project specific imports
from fastapi import APIRouter, Request, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

# Local imports
from ...db.models.board import BoardInDb
from .. import auth, dependencies, constants

router = APIRouter()

# -----------------------------------------------------------------------------#
# Datamodel
# -----------------------------------------------------------------------------#


class VerifiedUser(BaseModel):
    id: str
    name: str
    boards: list[BoardInDb]


# -----------------------------------------------------------------------------#
# Routes
# -----------------------------------------------------------------------------#


@router.post("/token", status_code=status.HTTP_200_OK, response_model=auth.Token)
async def create_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> auth.Token:
    user = await auth.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Invalid signin credentials"},
        )

    access_token_expires = timedelta(minutes=constants.ACCESS_TOKEN_EXPIRE_MINUTES)
    return auth.create_access_token(user, access_token_expires)


@router.get("/token", status_code=status.HTTP_200_OK, response_model=VerifiedUser)
async def get_verified_user(request: Request) -> VerifiedUser:
    token = request.headers["Authorization"]

    # Should return user info and boards
    user = auth._decode_token(token.split("Bearer ")[-1])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Please sign in again."},
        )

    boards = await dependencies.get_db_client().get_all_boards(user.id)
    return VerifiedUser(id=user.id, name=user.first_name, boards=boards)
