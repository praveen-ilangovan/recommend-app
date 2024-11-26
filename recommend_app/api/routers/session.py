"""
Authentication
"""

# Builtin imports
from typing import Annotated
from datetime import timedelta

# Project specific imports
from fastapi import APIRouter, HTTPException, status, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

# Local imports
from ... import ui
from .. import auth


# Constants
ACCESS_TOKEN_EXPIRE_MINUTES = 15

# Route
router = APIRouter()


# -----------------------------------------------------------------------------#
# Routes
# -----------------------------------------------------------------------------#
@router.get("/new")
async def show_login_page(request: Request) -> ui.JinjaTemplateResponse:
    """
    Show the login dialog to let the user log in.
    """
    return ui.show_page(request=request, name="login.html")


@router.post("/", status_code=status.HTTP_200_OK, response_model=auth.Token)
async def create_session(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> JSONResponse:
    user = await auth.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid signin credentials"
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = auth.create_access_token(user, access_token_expires)

    response = JSONResponse({"status": "authenticated"})
    response.set_cookie(token.name, token.access_token, httponly=True, secure=True)
    return response


@router.get("/logout", status_code=status.HTTP_200_OK)
async def delete_session(request: Request) -> ui.JinjaTemplateResponse:
    response = ui.show_page(request=request, name="login.html")
    response.delete_cookie(auth.OAUTH2_SCHEME.token_name)
    return response
