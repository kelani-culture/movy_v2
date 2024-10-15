from enum import Enum
from typing import Optional

from sqlalchemy import String, Text, Enum as SQLALCHEMY_ENUM
from sqlalchemy.orm import Mapped, mapped_column

from .base import AbstractBaseUser


class TheatreSignInEnum(Enum):
    PASSWORD = "password"
    INSTAGRAM = "instagram"
    X = "x"
    FACEBOOK = "Facebook"


class Theatre(AbstractBaseUser):
    __tablename__ = "theatres"
    name: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True, index=True
    )
    description: Mapped[str] = mapped_column(
        Text, nullable=True, doc="This columns hold the description about the cinema"
    )

    profile_pic: Mapped[Optional[str]] = mapped_column(String(100))
    provider: Mapped[Enum] = mapped_column(SQLALCHEMY_ENUM(TheatreSignInEnum), default=TheatreSignInEnum.PASSWORD)

    def __init__(
        self,
        theatre_name: str,
        email: str,
        password: str,
        profile_pic: Optional[str] = None,
    ):
        self.name = theatre_name
        self.email = email
        self.password = self.hash_password(password)
        profile_pic = profile_pic

    @property
    def get_fullname(self) -> str:
        return self.name