import uuid
from datetime import datetime
from typing import Optional

from nanoid import generate
from passlib.context import CryptContext
from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column

from database import Base

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


class AbstractBaseUser(Base):
    """
    An abstract base for both the User and theatre to inherit from...
    """

    __abstract__ = True
    id: Mapped[str] = mapped_column(
        String(100), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True
    )
    u_id: Mapped[str] = mapped_column(
        String(21),
        unique=True,
        default=lambda: generate(),
        nullable=False,
    )
    email: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False, index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, server_default=func.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(onupdate=func.now())
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    is_verified: Mapped[bool] = mapped_column(default=False)
    is_active: Mapped[bool] = mapped_column(default=True)

    def hash_password(self, password) -> str:
        return pwd_context.hash(password)

    def verify_password(self, raw_pass: str) -> bool:
        return pwd_context.verify(raw_pass, self.password)
