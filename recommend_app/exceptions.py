"""
module: exceptions

BaseRecommendException
"""


class RecommendAppError(BaseException):
    """
    Store the message as an attribute.
    """

    def __init__(self, message: str):
        self.message = message
