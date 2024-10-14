from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import AbstractBaseUser


class Theatre(AbstractBaseUser):
    __tablename__ = "theatres"
    name: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True, index=True
    )
    description: Mapped[str] = mapped_column(
        Text, nullable=True, doc="This columns hold the description about the cinema"
    )

    profile_pic: Mapped[str] = mapped_column(String(100))
