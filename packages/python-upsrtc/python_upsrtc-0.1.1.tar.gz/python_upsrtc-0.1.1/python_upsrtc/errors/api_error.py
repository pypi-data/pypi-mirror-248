
class apiError(Exception):
    """
    Raised when there is an api error.
    """
    def __init__(self, message):
        super().__init__(message)