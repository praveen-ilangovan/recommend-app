"""
All the users related routes

users
    GET     /users/new          - register form
    POST    /users              - Add the user to the db
    GET     /users/{id}         - Display user's public boards.
    PUT     /users/{id}         - Update user info :session

"""

# Builtin imports
from typing import Union

# Project specific imports
from fastapi import APIRouter, status, HTTPException, Request
from fastapi.responses import RedirectResponse, JSONResponse
from pydantic import BaseModel

# Local imports
from ...db.models.user import NewUser, UserInDb, UpdateUser
from ...db.models.board import BoardInDb
from ...db.exceptions import (
    RecommendDBModelCreationError,
    RecommendAppDbError,
    RecommendDBModelNotFound,
)
from .. import dependencies, auth, constants
from ... import ui

router = APIRouter()

# -----------------------------------------------------------------------------#
# Response Model
# -----------------------------------------------------------------------------#


class UserWithBoards(BaseModel):
    user: UserInDb
    boards: list[BoardInDb]


# -----------------------------------------------------------------------------#
# Routes
# -----------------------------------------------------------------------------#
@router.get("/new")
async def show_register_page(request: Request) -> ui.JinjaTemplateResponse:
    """
    Displays the register page for users to create a new account
    """
    return ui.show_page(request=request, name="register.html")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserInDb)
async def add_user(new_user: NewUser) -> UserInDb:
    try:
        user_in_db = await dependencies.get_db_client().add_user(new_user)
    except RecommendDBModelCreationError as err:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail={"error": err.message})

    return user_in_db


@router.get(
    "/{requested_user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserWithBoards,
)
async def show_user_page(
    request: Request,
    requested_user_id: str,
    user: auth.OPTIONAL_USER,
    show_page: bool = True,
) -> Union[RedirectResponse, ui.JinjaTemplateResponse, UserWithBoards]:
    if user and requested_user_id == user.id:
        return RedirectResponse(constants.ROUTES.ME)

    try:
        requested_user = await dependencies.get_db_client().get_user(requested_user_id)
        boards = await dependencies.get_db_client().get_all_boards(
            requested_user_id, only_public=True
        )
    except RecommendDBModelNotFound as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail={"error": err.message}
        )

    if show_page:
        return ui.show_page(
            request=request,
            name="user.html",
            context={"user": user, "requested_user": requested_user, "boards": boards},
        )

    return UserWithBoards(user=requested_user, boards=boards)


@router.put("/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(
    user_id: str, data: UpdateUser, user: auth.REQUIRED_USER
) -> JSONResponse:
    if not user or user.id != user_id:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Unauthorized to make this change"},
        )

    try:
        updated = await dependencies.get_db_client().update_user(user_id, data)
    except RecommendDBModelNotFound as err:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail={"error": err.message})
    except RecommendAppDbError as err:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail={"error": err.message})

    # Since the user information has been updated, we have to regenerate the access token.
    # Access token has information about the user.
    authorised_user = auth.AuthenticatedUser.from_dbuser(updated)
    return auth.create_access_token_set_cookie(authorised_user)
