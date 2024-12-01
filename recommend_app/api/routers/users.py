"""
All the users related routes

users
    GET     /users/new          - register form
    POST    /users              - Add the user to the db
    GET     /users/{id}         - Display user's public boards.
    PUT     /users/{id}         - Update user info :session

"""

# Project specific imports
from fastapi import APIRouter, status, HTTPException, Request
from fastapi.responses import RedirectResponse

# Local imports
from ...db.models.user import NewUser, UserInDb
from ...db.exceptions import RecommendDBModelCreationError
from .. import dependencies, auth, constants
from ... import ui

router = APIRouter()


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
    "/{requested_user_id}", status_code=status.HTTP_200_OK, response_model=UserInDb
)
async def show_user_page(
    request: Request, requested_user_id: str, user: auth.OPTIONAL_USER
) -> RedirectResponse | ui.JinjaTemplateResponse:
    if user and requested_user_id == user.id:
        return RedirectResponse(constants.ROUTES.ME)

    requested_user = await dependencies.get_db_client().get_user(requested_user_id)
    boards = await dependencies.get_db_client().get_all_boards(
        requested_user_id, only_public=True
    )
    return ui.show_page(
        request=request,
        name="user.html",
        context={"user": user, "requested_user": requested_user, "boards": boards},
    )
