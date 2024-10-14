class MovyBaseApiException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class UserAlreadyExistException(MovyBaseApiException): ...


class InvalidEmailOrPassword(MovyBaseApiException): ...


class AccountDisabled(MovyBaseApiException): ...


class EmailNotVerified(MovyBaseApiException): ...
