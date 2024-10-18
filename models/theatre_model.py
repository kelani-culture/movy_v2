from enum import Enum
from typing import List, Optional

from sqlalchemy import Column, ForeignKey, String, Table, Text
from sqlalchemy import Enum as SQLALCHEMY_ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

from .base import AbstractBaseUser


class TheatreSignInEnum(Enum):
    PASSWORD = "password"
    INSTAGRAM = "instagram"
    X = "x"
    FACEBOOK = "Facebook"


theatre_address = Table(
    "theatre_address",
    Base.metadata,
    Column("theatre_id", ForeignKey("theatres.id", ondelete="CASCADE")),
    Column("address_id", ForeignKey("address.id")),
)


class Theatre(AbstractBaseUser):
    __tablename__ = "theatres"
    name: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True, index=True
    )
    description: Mapped[str] = mapped_column(
        Text, nullable=True, doc="This columns hold the description about the cinema"
    )

    profile_pic: Mapped[Optional[str]] = mapped_column(String(100))
    provider: Mapped[Enum] = mapped_column(
        SQLALCHEMY_ENUM(TheatreSignInEnum), default=TheatreSignInEnum.PASSWORD
    )
    is_admin: Mapped[bool] = mapped_column(default=True)

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

    addresses: Mapped[List["Address"]] = relationship(
        secondary=theatre_address, back_populates="theatres"
    )

    @property
    def get_fullname(self) -> str:
        return self.name

    def __str__(self):
        return self.name


class Address(Base):
    __tablename__ = "address"
    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, nullable=False
    )
    street_address: Mapped[str] = mapped_column(String(500), index=True)
    city: Mapped[str] = mapped_column(String(100), index=True)
    state: Mapped[str] = mapped_column(String(100), index=True)

    theatres: Mapped[List[Theatre]] = relationship(
        secondary=theatre_address, back_populates="addresses"
    )

    def __str__(self):
        return f"{self.street_address} - {self.city} - {self.state}"
