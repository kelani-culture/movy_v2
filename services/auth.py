from datetime import datetime
from typing import Dict

from fastapi import Depends, UploadFile
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from database import get_db
from exception import (
    AccountDisabled,
    BearerNotFoundInParsedToken,
    EmailNotVerified,
    InvalidEmailOrPassword,
    PermissionNotAllowed,
    UserAlreadyExistException,
    UserNotFound,
)
from models.theatre_model import Theatre
from models.user_model import User
from schemas.settings import STATIC_DIRECTORY
from utils.handle_image import image_upload
from utils.jwt_token import decode_user_token, generate_user_token

USER_TYPE_MODEL = {"user": User, "theatre": Theatre}


oauth_2_scheme = HTTPBearer()


def create_user(db: Session, type_user: str = "user", **kwargs):
    """
    Handle user registration into the application
    """
    model = USER_TYPE_MODEL[type_user]
    user = db.query(model).filter(model.email == kwargs["email"]).one_or_none()

    if type_user == "user":  # check if email exist in theatre table
        theatre = db.query(Theatre).filter(Theatre.email == kwargs["email"]).first()
        if theatre:
            raise UserAlreadyExistException("This email has already been taken")

    elif type_user == "theatre":  # check if email exist in user table
        user_check = db.query(User).filter(User.email == kwargs["email"]).first()
        if user_check:
            raise UserAlreadyExistException("This email has already been taken")

    if user:
        raise UserAlreadyExistException(
            "User email already exists please proceed to login"
        )

    user = model(**kwargs)

    # FIXME fix this before pushing to production make  user are able to verify email
    # before enabling verify_true this is for dev purpose only and basically because I am lazy to setup email verifcation
    # and basically I am lazy
    user.is_verified = True
    db.add(user)
    db.commit()

    # TODO handle user email verification...


async def user_login(
    db: Session, type_user: str = "user", **kwargs
) -> Dict[str, str | int]:
    """
    handle user login routes
    """
    model = USER_TYPE_MODEL[type_user]

    user = db.query(model).filter(model.email == kwargs["email"]).one_or_none()

    if not user:
        raise InvalidEmailOrPassword("Invalid email or password provided")

    if not user.is_active:
        raise AccountDisabled("Your account has been disabled please contact admin")

    if not user.is_verified:
        raise EmailNotVerified(
            "Your account has not been verified please check your inbox"
        )

    v_pass = user.verify_password(kwargs["password"])
    if not v_pass:
        raise InvalidEmailOrPassword("Invalid email or password provided")

    # user token generation
    user_token = generate_user_token(user, type_user)

    if type_user == "user":
        user_token["full_name"] = user.get_fullname
    else:
        user_token["theatre_name"] = user.get_fullname

    user_token["email"] = user.email
    user_token["profile_pic"] = user.profile_pic
    return user_token


def get_current_user_or_theatre(
    payload: HTTPAuthorizationCredentials = Depends(oauth_2_scheme),
    db: Session = Depends(get_db),
) -> Theatre | User:
    """
    get the current user either a regular user or a theatre
    """
    if not payload.scheme == "Bearer":
        raise BearerNotFoundInParsedToken("Invalid token provided")
    token = payload.credentials
    user_info = decode_user_token(token)

    user = db.query(User).filter(User.email == user_info.email).one_or_none()
    if not user:
        user = db.query(Theatre).filter(Theatre.email == user_info.email).one_or_none()

    if not user:
        raise UserNotFound("User email not registered")

    return user


def update_profile_pic(
    db: Session, file: UploadFile, obj: User | Theatre, type_user: str = "user"
) -> str:
    """
    handle user profile update
    """

    file_location = (
        STATIC_DIRECTORY
        / "profile_pic"
        / type_user
        / f"{datetime.date(datetime.now())}"
    )
    obj.profile_pic = image_upload(file_location, file)
    db.commit()
    db.refresh(obj)

    return obj.profile_pic


def get_user(user: User = Depends(get_current_user_or_theatre)) -> User:
    if not isinstance(user, User):
        raise PermissionNotAllowed("Theatre not allowed")
    return user


def get_theatre(theatre: Theatre = Depends(get_current_user_or_theatre)) -> Theatre:
    if not isinstance(theatre, Theatre) and theatre.is_admin is False:
        raise PermissionNotAllowed("User not allowed")

    return theatre
