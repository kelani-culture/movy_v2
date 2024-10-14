from typing import Dict

from sqlalchemy.orm import Session

from exception import (
    AccountDisabled,
    EmailNotVerified,
    InvalidEmailOrPassword,
    UserAlreadyExistException,
)
from models.theatre_model import Theatre
from models.user_model import User
from utils.token import generate_user_token

USER_TYPE_MODEL = {"user": User, "theatre": Theatre}


def create_user(db: Session, type_user: str = "user", **kwargs):
    """
    Handle user registration into the application
    """
    model = USER_TYPE_MODEL[type_user]
    user = db.query(model).filter(model.email == kwargs["email"]).one_or_none()

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

    #TODO handle user email verification...


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
        user_token["theatre_name"] = user.get_name

    user_token["email"] = user.email
    user_token["profile_pic"] = user.profile_pic
    return user_token
