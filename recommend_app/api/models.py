"""
API specific data models. Mostly used to Request and Responses
"""

# Project specific imports
from pydantic import BaseModel

# Local imports
from ..db.models.user import UserInDb
from ..db.models.board import BoardInDb
from ..db.models.card import CardInDb
from .auth import AuthenticatedUser

# -----------------------------------------------------------------------------#
# Models
# -----------------------------------------------------------------------------#


class AuthUserWithBoards(BaseModel):
    user: AuthenticatedUser
    boards: list[BoardInDb]


class UserWithBoards(BaseModel):
    user: UserInDb
    boards: list[BoardInDb]


class BoardWithCards(BaseModel):
    board: BoardInDb
    cards: list[CardInDb]


class BoardAndCard(BaseModel):
    board: BoardInDb
    card: CardInDb
