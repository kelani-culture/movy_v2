from typing import Callable

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from exception import (
    AccountDisabled,
    EmailNotVerified,
    InvalidEmailOrPassword,
    MovyBaseApiException,
    UserAlreadyExistException,
)
from routers.users import routers as user_router

app = FastAPI()


app.include_router(user_router)


def create_exception_handler(
    status_code: int, err_msg: str
) -> Callable[[Request, MovyBaseApiException], JSONResponse]:
    detail = {"message": err_msg}

    async def exception_handler(_: Request, exc: MovyBaseApiException) -> JSONResponse:
        if exc.message:
            detail["message"] = exc.message

        return JSONResponse(
            status_code=status_code, content={"message": detail["message"]}
        )

    return exception_handler


app.add_exception_handler(
    exc_class_or_status_code=UserAlreadyExistException,
    handler=create_exception_handler(
        status_code=status.HTTP_400_BAD_REQUEST, err_msg="User already exist"
    ),
)

app.add_exception_handler(
    exc_class_or_status_code=InvalidEmailOrPassword,
    handler=create_exception_handler(
        status_code=status.HTTP_400_BAD_REQUEST,
        err_msg="Invalid email or password provided",
    ),
)

app.add_exception_handler(
    exc_class_or_status_code=AccountDisabled,
    handler=create_exception_handler(
        status_code=status.HTTP_400_BAD_REQUEST,
        err_msg="Your account is disable please contact admin",
    ),
)


app.add_exception_handler(
    exc_class_or_status_code=EmailNotVerified,
    handler=create_exception_handler(
        status_code=status.HTTP_400_BAD_REQUEST,
        err_msg="Your email not yet verified please contact admin",
    ),
)
