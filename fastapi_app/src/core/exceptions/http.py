class AppException(Exception):
    def __init__(self, message: str, code: str = "error"):
        self.message = message
        self.code = code


class NotFoundError(AppException):
    pass


class BadRequestError(AppException):
    pass


class ConflictError(AppException):
    pass


class ForbiddenError(AppException):
    pass


class UnauthorizedError(AppException):
    pass


class DomainValidationError(AppException):
    pass


class InternalError(AppException):
    pass