"""
OAuth related functionality
"""

# Builtin imports
from typing import Any, Optional, Annotated, TYPE_CHECKING
from datetime import datetime, timezone, timedelta

# Project specific imports
from fastapi import Depends, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError

# Local imports
from . import dependencies, constants
from ..db.exceptions import RecommendAppDbError, RecommendDBModelNotFound
from ..db.hashing import Hasher

if TYPE_CHECKING:
    from ..db.models.user import UserInDb


# -----------------------------------------------------------------------------#
# OAUTH extensions
# -----------------------------------------------------------------------------#
async def get_token_from_header(
    request: Request, key: str = "Authorization"
) -> Optional[str]:
    """
    Grab the authorization key from the request header. Check if it has
    Bearer scheme credential and if so, return the token.

    Args:
        request (Request): The incoming request

    Returns:
        Return the token if there is valid crentional if not returns None
    """
    value = request.headers.get(key)
    if not value:
        return None

    credentials = value.split()
    if not credentials or len(credentials) != 2 or credentials[0] != "Bearer":
        return None

    if credentials[1] and credentials[1] != "undefined":
        return credentials[1]

    return None


def get_token_from_cookie(request: Request, cookie_name: str) -> Optional[str]:
    """
    Grab the access token from the cookies.
    """
    return request.cookies.get(cookie_name)


class OAuth2PasswordCookie(OAuth2PasswordBearer):
    """
    OAuth2 password flow with token in a httpOnly cookie

    DISCUSSION: https://github.com/fastapi/fastapi/discussions/9142
    LINK: https://github.com/kthwaite/fastapi-jwt-cookies/tree/master
    """

    def __init__(self, *args, token_name: Optional[str] = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.__token_name = token_name or "access_token"

    @property
    def token_name(self) -> str:
        """Get the name of the token's cookie."""
        return self.__token_name

    async def __call__(self, request: Request) -> Optional[str]:
        """Extract and return a JWT from the request cookies.

        Raises:
            HTTPException: 403 error if no token cookie is present.
        """
        token = await get_token_from_header(request)
        if token:
            return token
        return get_token_from_cookie(request, self.__token_name)


# -----------------------------------------------------------------------------#
# JWT Constants
# -----------------------------------------------------------------------------#
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
OAUTH2_SCHEME = OAuth2PasswordCookie(
    tokenUrl="session", auto_error=False, token_name="access_token"
)

# -----------------------------------------------------------------------------#
# Models
# -----------------------------------------------------------------------------#


class Token(BaseModel):
    name: str
    access_token: str
    token_type: str


class AuthenticatedUser(BaseModel):
    sub: str
    email_address: str
    id: str
    user_name: str
    first_name: str
    last_name: str
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None

    # -------------------------------------------------------------------------#
    # Methods
    # -------------------------------------------------------------------------#
    @classmethod
    def from_payload(cls, payload: dict[str, Any]) -> "AuthenticatedUser":
        """
        Create an authenticated user from the payload
        """
        return cls(
            sub=payload["sub"],
            email_address=payload["email_address"],
            id=payload["id"],
            user_name=payload["user_name"],
            first_name=payload["first_name"],
            last_name=payload["last_name"],
        )

    @classmethod
    def from_dbuser(cls, user: "UserInDb") -> "AuthenticatedUser":
        """
        Create an authenticated user from the payload
        """
        return cls(
            sub=user.email_address,
            email_address=user.email_address,
            id=user.id,
            user_name=user.user_name,
            first_name=user.first_name,
            last_name=user.last_name,
        )


# -----------------------------------------------------------------------------#
# Methods
# -----------------------------------------------------------------------------#


async def authenticate_user(
    emailOrUserName: str, password: str
) -> Optional[AuthenticatedUser]:
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

    return AuthenticatedUser.from_dbuser(user)


def create_token(name: str, data: dict[str, Any], expires_delta: timedelta) -> Token:
    """
    Create a JWT token for the given data
    """
    expire = datetime.now(timezone.utc) + expires_delta
    data.update({"exp": expire})

    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return Token(name=name, access_token=access_token, token_type="bearer")


def create_access_token(user: AuthenticatedUser, expires_delta: timedelta) -> Token:
    """
    Using the data of the user, create a json token.
    """
    return create_token(OAUTH2_SCHEME.token_name, user.model_dump(), expires_delta)


def create_access_token_set_cookie(user: AuthenticatedUser) -> JSONResponse:
    """
    For the given user, create an access token and return a JSONResponse that
    sets the token as a cookie. This is being used by create_session and update_user

    Args:
        user (AuthenticatedUser): The current signed in user

    Returns:
        A JsonResponse that sets the cookie
    """
    access_token_expires = timedelta(minutes=constants.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(user, access_token_expires)

    response = JSONResponse({"status": "authenticated"})
    response.set_cookie(token.name, token.access_token, httponly=True, secure=True)
    return response


def create_refresh_token(user: AuthenticatedUser, expires_delta: timedelta) -> Token:
    """
    Using the data of the user, create a json token.
    """
    return create_token("refresh_token", {"sub": user.sub}, expires_delta)


def _decode_token(token: str) -> Optional[AuthenticatedUser]:
    """
    Decode the token and if its active, convert the payload to an authenticated
    user object
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except (InvalidTokenError, ExpiredSignatureError):
        return None

    # Convert payload to an authenticated user
    authenticate_user = AuthenticatedUser.from_payload(payload)
    authenticate_user.access_token = token
    return authenticate_user


async def _decode_refresh_token(token: str) -> Optional[AuthenticatedUser]:
    """
    Decode the refresh token and get the authenticated user form the payload
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except (InvalidTokenError, ExpiredSignatureError):
        return None

    try:
        user = await dependencies.get_db_client().get_user(email_address=payload["sub"])
    except (RecommendAppDbError, RecommendDBModelNotFound):
        return None

    # Convert payload to an authenticated user
    return AuthenticatedUser.from_dbuser(user)


async def get_user(
    token: Annotated[str, Depends(OAUTH2_SCHEME)],
) -> Optional[AuthenticatedUser]:
    """
    Get the user object from the access token.

    Args:
        token (str): Access Token (Read from the cookies)

    Returns:
        `AuthenticatedUser` - If a user is logged in. if not, returns None
    """
    return _decode_token(token)


async def get_authenticated_user(
    token: Annotated[str, Depends(OAUTH2_SCHEME)],
) -> AuthenticatedUser:
    """
    Get the authenticated user from the access token. The token is validated and
    made sure its still active before converting the token's payload into an
    authenticated user object

    Args:
        token (str): Access Token (Read from the cookies)

    Returns:
        `AuthenticatedUser` - If a user is logged in. if not, returns None

    Raises:
        `RecommendAppRequiresLogin`
    """
    user = _decode_token(token)
    if not user:
        # raise RecommendAppRequiresLogin("This page requires login")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "This page requires login"},
        )
    return user


# -----------------------------------------------------------------------------#
# Dependency
# -----------------------------------------------------------------------------#
OPTIONAL_USER = Annotated[Optional[AuthenticatedUser], Depends(get_user)]
REQUIRED_USER = Annotated[AuthenticatedUser, Depends(get_authenticated_user)]
