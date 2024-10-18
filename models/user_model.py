from enum import Enum
from typing import Optional

from sqlalchemy import Enum as SQLALCHEMY_ENUM
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import AbstractBaseUser


class SignInProvider(Enum):
    GOOGLE = "google"
    PASSWORD = "password"


class User(AbstractBaseUser):
    __tablename__ = "users"
    first_name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    profile_pic: Mapped[Optional[str]] = mapped_column(String(100))
    provider: Mapped[Enum] = mapped_column(
        SQLALCHEMY_ENUM(SignInProvider), nullable=False, default=SignInProvider.PASSWORD
    )

    def __init__(
        self,
        first_name: str,
        last_name: str,
        email: str,
        password: str,
        profile_pic: Optional[str] = None,
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = self.hash_password(password)
        profile_pic = profile_pic

    @property
    def get_fullname(self) -> str:
        return f"{self.last_name} {self.first_name}"

    def __str__(self):
        return f"{self.last_name} - {self.first_name}"
