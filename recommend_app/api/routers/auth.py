"""
Authentication
"""

# Builtin imports
from typing import Annotated, TYPE_CHECKING, Optional

# Project specific imports
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# Local imports
from .. import dependencies
from ...db.exceptions import RecommendAppDbError, RecommendDBModelNotFound
from ...db.hashing import Hasher

if TYPE_CHECKING:
    from ...db.models.user import UserInDb


# JWT
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

# Route
router = APIRouter()


# -----------------------------------------------------------------------------#
# Methods
# -----------------------------------------------------------------------------#
async def authenticate_user(email_address: str, password: str) -> Optional["UserInDb"]:
    """
    Authenticate the user using the email address and the password.
    """
    try:
        user = await dependencies.get_db_client().get_user(email_address=email_address)
    except (RecommendAppDbError, RecommendDBModelNotFound):
        return None

    verified = Hasher.verify_password(password, user.password)
    if not verified:
        return None

    return user


async def get_current_user():
    """
    Get the current user.

    Relies on OAuth login form to request the user to provide the login
    credentials. The credientials are checked and once it is authenticated,
    an UserInDb object is returned.
    """


# -----------------------------------------------------------------------------#
# Routes
# -----------------------------------------------------------------------------#


@router.post("/token", status_code=status.HTTP_201_CREATED)
async def signin_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid signin credentials"
        )

    return user  # type: ignore

    # access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # access_token = create_access_token(
    #     data={"sub": user.email_address, "id": user.id, "role": user.role}, expires_delta=access_token_expires
    # )

    # return Token(access_token=access_token, token_type="bearer")
