"""
RecommendApp API specific exceptions
"""


class RecommendAppRequiresLogin(Exception):
    """
    App throws this error when the user tries to access a page thats requires
    the user to be logged in
    """
