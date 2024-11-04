class MovyBaseApiException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class UserAlreadyExistException(MovyBaseApiException): ...


class InvalidEmailOrPassword(MovyBaseApiException): ...


class AccountDisabled(MovyBaseApiException): ...


class EmailNotVerified(MovyBaseApiException): ...


class InvalidAccessTokenProvided(MovyBaseApiException): ...


class BearerNotFoundInParsedToken(MovyBaseApiException): ...


class UserNotFound(MovyBaseApiException): ...


class ImageErrorException(MovyBaseApiException): ...



class TheatreHallException(MovyBaseApiException): ...


class MovieException(MovyBaseApiException): ...

class PermissionNotAllowed(MovieException): ...