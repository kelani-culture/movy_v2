from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import AbstractBaseUser


class User(AbstractBaseUser):
    __tablename__ = "users"
    first_name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    is_admin: Mapped[bool] = mapped_column(default=False)
