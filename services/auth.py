from sqlalchemy.orm import Session

from exception import UserAlreadyExistException
from models.theatre_model import Theatre
from models.user_model import User

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
    db.add(user)
    db.commit()
