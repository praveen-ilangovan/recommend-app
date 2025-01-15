"""
A set of special endpoints for browser extension.

Browser extensions send the Authorization token in the request header.
"""

# Builtin imports
import json
from datetime import timedelta

# Project specific imports
from fastapi import APIRouter, Request, status, HTTPException

# Local imports
from .. import auth, constants

router = APIRouter()

# -----------------------------------------------------------------------------#
# Functions
# -----------------------------------------------------------------------------#


def reissue_token(request: Request) -> auth.AuthenticatedUser:
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

    user.access_token = access_token
    return user
