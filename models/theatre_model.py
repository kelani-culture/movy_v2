from enum import Enum
from typing import List, Optional

from sqlalchemy import (
    Column,
    CheckConstraint,
    ForeignKey,
    String,
    Table,
    Text,
    UniqueConstraint,
)
from sqlalchemy import Enum as SQLALCHEMY_ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

from .base import AbstractBaseUser


class TheatreSignInEnum(Enum):
    PASSWORD = "password"
    INSTAGRAM = "instagram"
    X = "x"
    FACEBOOK = "Facebook"


class SeatStatus(Enum):
    AVAILABLE = "Available"
    RESERVED = "Reserved"
    BOOKED = "Booked"


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

    theatre_halls: Mapped[List["TheatreHall"]] = relationship(
        "TheatreHall", back_populates="theatre"
    )


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


class TheatreHall(Base):
    __tablename__ = "theatre_halls"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(20), unique=True)

    capacity: Mapped[int]
    total_row: Mapped[int] = mapped_column(default=0)
    seats_per_row: Mapped[int] = mapped_column(default=0)

    theatre_id: Mapped[str] = mapped_column(ForeignKey("theatres.id"))
    theatre: Mapped[Theatre] = relationship(Theatre, back_populates="theatre_halls")
    seats: Mapped[List["Seat"]] = relationship("Seat", back_populates="theatre_halls")

    __table_args__ = (
        CheckConstraint("total_rows >= 0", name="check_total_rows_non_negative"),
        CheckConstraint("seats_per_row >= 0", name="check_seats_per_row_non_negative"),
    )

    def __str__(self):
        return self.name


class Seat(Base):
    __tablename__ = "seats"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    row_name: Mapped[str] = mapped_column(String(1))
    seat: Mapped[int]

    status: Mapped[Enum] = mapped_column(
        SQLALCHEMY_ENUM(SeatStatus), default=SeatStatus.AVAILABLE
    )

    theatre_hall_id: Mapped[int] = mapped_column(ForeignKey("theatre_halls.id"))
    theatre_halls: Mapped[TheatreHall] = relationship(
        TheatreHall, back_populates="seats"
    )

    __table_args__ = (
        UniqueConstraint("row_name", "seat", "theatre_hall_id", name="uq_theatre_hall_id_row_name_seat_row"),
    )
