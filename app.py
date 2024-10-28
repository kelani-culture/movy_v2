from typing import Callable

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from exception import (
    AccountDisabled,
    BearerNotFoundInParsedToken,
    EmailNotVerified,
    ImageErrorException,
    InvalidAccessTokenProvided,
    InvalidEmailOrPassword,
    MovyBaseApiException,
    UserAlreadyExistException,
    UserNotFound,
)
from routers.theatre import profile_routers as theatre_profile_routes
from routers.theatre import routers as theatre_router
from routers.users import profile as user_profile_routes
from routers.users import routers as user_router
from schemas.settings import STATIC_DIRECTORY

app = FastAPI()


app.include_router(user_router)
app.include_router(user_profile_routes)
app.include_router(theatre_profile_routes)
app.include_router(theatre_router)


# static file location


# app.mount("/profile_pic", StaticFiles(directory=UPLOAD_DIRECTORY), name="profile_pic")
app.mount("/static", StaticFiles(directory=STATIC_DIRECTORY), name="static")


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


app.add_exception_handler(
    exc_class_or_status_code=InvalidAccessTokenProvided,
    handler=create_exception_handler(
        status_code=status.HTTP_401_UNAUTHORIZED,
        err_msg="Invalid token provided",
    ),
)


app.add_exception_handler(
    exc_class_or_status_code=BearerNotFoundInParsedToken,
    handler=create_exception_handler(
        status_code=status.HTTP_401_UNAUTHORIZED, err_msg="Invalid token provided"
    ),
)

app.add_exception_handler(
    exc_class_or_status_code=UserNotFound,
    handler=create_exception_handler(
        status_code=status.HTTP_404_NOT_FOUND, err_msg="Invalid token provided"
    ),
)


app.add_exception_handler(
    exc_class_or_status_code=ImageErrorException,
    handler=create_exception_handler(
        status_code=status.HTTP_400_BAD_REQUEST, err_msg="Invalid image file"
    ),
)
