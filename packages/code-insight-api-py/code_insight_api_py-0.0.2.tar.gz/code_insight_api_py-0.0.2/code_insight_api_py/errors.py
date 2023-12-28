class GenericError(Exception):
    """Generic error class, catch-all for most code insight API errors."""
    pass

class NotYetImplementedError(Exception):
    """Error class for API features that have not yet been implemented."""
    pass
