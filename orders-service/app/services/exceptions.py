"""Service Exceptions."""


class ServiceException(Exception):
    """Service Exception."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class ValidationErrorsException(ServiceException):
    """Validation Errors Exception."""


class InvalidOrderQuantityException(ServiceException):
    """Invalid Order Quantity Exception."""
