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
from .. import auth, constants

# Route
router = APIRouter()


# -----------------------------------------------------------------------------#
# Routes
# -----------------------------------------------------------------------------#


@router.post("/", status_code=status.HTTP_200_OK, response_model=auth.AuthenticatedUser)
async def create_session(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], set_cookie: bool = False
) -> JSONResponse | auth.AuthenticatedUser:
    user = await auth.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Invalid signin credentials"},
        )

    if set_cookie:
        return auth.create_access_token_set_cookie(user)

    access_token_expires = timedelta(minutes=constants.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = auth.create_access_token(user, access_token_expires)
    user.access_token = token.access_token
    return user


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_session(request: Request) -> ui.JinjaTemplateResponse:
    response = ui.show_page(request=request, name="login.html")
    response.delete_cookie(auth.OAUTH2_SCHEME.token_name)
    return response
