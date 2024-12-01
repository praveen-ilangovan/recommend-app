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
    LOGOUT = "/session/logout"

    # users
    REGISTER = "/users/new"
    ADD_USER = "/users/"
    USER_BOARDS = "/users/{user_id}"

    # boards
    CREATE_BOARD = "/boards/new"
    ADD_BOARD = "/boards/"
    GET_BOARD = "/boards/{board_id}"
