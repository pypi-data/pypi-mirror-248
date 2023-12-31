
class noBusStopFoundError(Exception):
    """
    Raised when No bus stop is found.
    """
    def __init__(self, message):
        super().__init__(message)