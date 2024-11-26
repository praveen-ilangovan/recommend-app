"""
Authentication
"""

# Builtin imports
from typing import Annotated, TYPE_CHECKING, Optional, Any
from datetime import datetime, timezone, timedelta

# Project specific imports
from fastapi import APIRouter, HTTPException, status, Depends, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from pydantic import BaseModel

# Local imports
from .. import dependencies
from ...db.exceptions import RecommendAppDbError, RecommendDBModelNotFound
from ...db.hashing import Hasher
from ... import ui

if TYPE_CHECKING:
    from ...db.models.user import UserInDb


# JWT
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="session")

# Route
router = APIRouter()

# -----------------------------------------------------------------------------#
# Models
# -----------------------------------------------------------------------------#


class Token(BaseModel):
    access_token: str
    token_type: str


# -----------------------------------------------------------------------------#
# Methods
# -----------------------------------------------------------------------------#
async def authenticate_user(
    emailOrUserName: str, password: str
) -> Optional["UserInDb"]:
    """
    Authenticate the user using the email address and the password.
    """
    try:
        if "@" in emailOrUserName:
            user = await dependencies.get_db_client().get_user(
                email_address=emailOrUserName
            )
        else:
            user = await dependencies.get_db_client().get_user(
                user_name=emailOrUserName
            )
    except (RecommendAppDbError, RecommendDBModelNotFound):
        return None

    verified = Hasher.verify_password(password, user.password)
    if not verified:
        return None

    return user


def create_access_token(data: dict[str, Any], expires_delta: timedelta) -> str:
    """
    Using the data of the user, create a json token.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})

    encoded = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded


async def get_current_user(token: Annotated[str, Depends(OAUTH2_SCHEME)]):
    """
    Get the current user.

    Relies on OAuth login form to request the user to provide the login
    credentials. The credientials are checked and once it is authenticated,
    an UserInDb object is returned.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email_address = payload.get("sub")
        id = payload.get("id")
        user_name = payload.get("user_name")
        if not all([email_address, id, user_name]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
            )

        return {"email_address": email_address, "id": id, "user_name": user_name}

    except jwt.exceptions.InvalidTokenError as err:
        print(err)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )


# -----------------------------------------------------------------------------#
# Routes
# -----------------------------------------------------------------------------#
@router.get("/new")
async def show_login_page(request: Request) -> ui.JinjaTemplateResponse:
    """
    Show the login dialog to let the user log in.
    """
    return ui.show_page(request=request, name="login.html")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Token)
async def create_session(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid signin credentials"
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email_address, "user_name": user.user_name, "id": user.id},
        expires_delta=access_token_expires,
    )

    return Token(access_token=access_token, token_type="bearer")
