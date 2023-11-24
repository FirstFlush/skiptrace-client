

class PasswordError(BaseException):
    """Raised when a user enters an incorrect password"""
    pass


class SpiderNotFound(BaseException):
    """Raised when user attempts to launch a spider that doesn't exist."""
    pass