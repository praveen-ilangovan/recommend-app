"""
Constants
"""


class ROUTES:
    # root

    # me
    ME = "/me/"

    # session
    CREATE_SESSION = "/session/"
    CREATE_SESSION_WITH_COOKIE = "/session/?set_cookie=true"
    LOGOUT = "/session/"

    # users
    ADD_USER = "/users/"
    SHOW_USER = "/users/{user_id}"
    GET_USER = "/users/{user_id}"
    UPDATE_USER = "/users/{user_id}"

    # boards
    ADD_BOARD = "/boards/"
    SHOW_BOARD = "/boards/{board_id}"
    GET_BOARD = "/boards/{board_id}"
    UPDATE_BOARD = "/boards/{board_id}"
    DELETE_BOARD = "/boards/{board_id}"

    # cards
    ADD_CARD = "/boards/{board_id}/cards"
    SHOW_CARD = "/cards/{card_id}"
    GET_CARD = "/cards/{card_id}"
    UPDATE_CARD = "/cards/{card_id}"
    DELETE_CARD = "/cards/{card_id}"

    # scrapper
    SCRAP = "/scrapper/?url={url}"

    # extension
    CREATE_TOKEN = "/extension/token"
    GET_VERIFIED_USER = "/extension/token"
    ADD_CARD_FROM_EXTN = "extension/{board_id}/cards"

    # Internal
    INTERNAL_LANDING = "/internal/"
    INTERNAL_REGISTER = "/internal/users/new"
    INTERNAL_LOGIN = "/internal/session/new"
    INTERNAL_CREATE_BOARD = "internal/boards/new"
    INTERNAL_CREATE_CARD = "/internal/boards/{board_id}/cards/new"
    INTERNAL_HEALTH = "/internal/health"


ACCESS_TOKEN_EXPIRE_MINUTES = 1
