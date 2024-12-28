"""
Constants
"""


class ROUTES:
    # root
    HEALTH = "/health"

    # me
    SHOW_ME = "/me/"
    ME = "/me/?show_page=false"

    # session
    LOGIN = "/session/new"
    CREATE_SESSION = "/session/"
    LOGOUT = "/session/"

    # users
    REGISTER = "/users/new"
    ADD_USER = "/users/"
    SHOW_USER = "/users/{user_id}"
    GET_USER = "/users/{user_id}?show_page=false"
    UPDATE_USER = "/users/{user_id}"

    # boards
    CREATE_BOARD = "/boards/new"
    ADD_BOARD = "/boards/"
    SHOW_BOARD = "/boards/{board_id}"
    GET_BOARD = "/boards/{board_id}?show_page=false"
    UPDATE_BOARD = "/boards/{board_id}"
    DELETE_BOARD = "/boards/{board_id}"

    # cards
    CREATE_CARD = "/{board_id}/cards/new"
    ADD_CARD = "/boards/{board_id}/cards"
    SHOW_CARD = "/cards/{card_id}"
    GET_CARD = "/cards/{card_id}?show_page=false"
    UPDATE_CARD = "/cards/{card_id}"
    DELETE_CARD = "/cards/{card_id}"

    # scrapper
    SCRAP = "/scrapper/?url={url}"

    # extension
    CREATE_TOKEN = "/extension/token"
    GET_VERIFIED_USER = "/extension/token"
    ADD_CARD_FROM_EXTN = "extension/{board_id}/cards"


ACCESS_TOKEN_EXPIRE_MINUTES = 15
