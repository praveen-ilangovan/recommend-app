"""
All the users related routes

users
    GET     /users/new          - register form
    POST    /users              - Add the user to the db
    GET     /users/{id}         - Get the user info and display it
    PUT     /users/{id}         - Update user info :session
    GET     /users/{id}/boards  - Get all the boards of this user

"""

# Project specific imports
from fastapi import APIRouter, status, HTTPException, Request

# Local imports
from ...db.models.user import NewUser, UserInDb
from ...db.exceptions import RecommendDBModelCreationError
from .. import dependencies
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
