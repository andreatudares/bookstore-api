"""Database Operations Exception."""


class DatabaseException(Exception):
    """Database Exception."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class DatabaseNotFoundException(DatabaseException):
    """Database Not Found Exception."""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class DatabaseAlreadyExistsException(DatabaseException):
    """Database Already Exists Exception."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
