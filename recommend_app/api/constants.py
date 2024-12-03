"""
Constants
"""


class ROUTES:
    # root
    HEALTH = "/health"

    # me
    ME = "/me/"

    # session
    LOGIN = "/session/new"
    CREATE_SESSION = "/session/"
    LOGOUT = "/session/"

    # users
    REGISTER = "/users/new"
    ADD_USER = "/users/"
    GET_USER = "/users/{user_id}"
    UPDATE_USER = "/users/{user_id}"

    # boards
    CREATE_BOARD = "/boards/new"
    ADD_BOARD = "/boards/"
    GET_BOARD = "/boards/{board_id}"
    UPDATE_BOARD = "/boards/{board_id}"
    DELETE_BOARD = "/boards/{board_id}"


ACCESS_TOKEN_EXPIRE_MINUTES = 15
