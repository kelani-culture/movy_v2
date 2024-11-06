from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from time import time
from typing import List, Optional

from nanoid import generate
from sqlalchemy import (
    CheckConstraint,
    Column,
    ForeignKey,
    Numeric,
    String,
    Table,
    Text,
    Time,
    UniqueConstraint,
    func,
)
from sqlalchemy import Enum as SQLALCHEMY_ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

from .base import AbstractBaseUser
from .movie_model import Movie
from .user_model import User


class TheatreSignInEnum(Enum):
    PASSWORD = "password"
    INSTAGRAM = "instagram"
    X = "x"
    FACEBOOK = "Facebook"


class SeatStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    RESERVED = "RESERVED"
    BOOKED = "BOOKED"


theatre_address = Table(
    "theatre_address",
    Base.metadata,
    Column("theatre_id", ForeignKey("theatres.id", ondelete="CASCADE")),
    Column("address_id", ForeignKey("address.id")),
)


booking_seats = Table(
    "booking_seat",
    Base.metadata,
    Column("seat_id", ForeignKey("seats.id")),
    Column("booking_id", ForeignKey("booking.id")),
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

    booking: Mapped["Booking"] = relationship("Booking", back_populates="theatre_halls")
    seat_booked: Mapped["SeatBooked"] = relationship(
        "SeatBooked", back_populates="theatre_halls"
    )
    showtime: Mapped["ShowTime"] = relationship(
        "ShowTime", back_populates="theatre_halls"
    )
    __table_args__ = (
        CheckConstraint("total_row >= 0", name="check_total_rows_non_negative"),
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
    booking: Mapped[List["Booking"]] = relationship(
        secondary=booking_seats, back_populates="seats"
    )

    __table_args__ = (
        UniqueConstraint(
            "row_name",
            "seat",
            "theatre_hall_id",
            name="uq_theatre_hall_id_row_name_seat_row",
        ),
    )

    def __str__(self):
        return f"{self.row_name} {self.seat} theatre_hall -> {self.theatre_hall_id}"

    def __repr__(self):
        return self.__str__()


class ShowTime(Base):
    __tablename__ = "show_time"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    u_id: Mapped[str] = mapped_column(
        String(100), default=lambda: generate(), unique=True
    )
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"))
    theatre_hall_id: Mapped[int] = mapped_column(ForeignKey("theatre_halls.id"))
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=0)
    stream_date: Mapped[date] = mapped_column(nullable=False)
    start_time: Mapped[time] = mapped_column(Time, nullable=False)
    end_time: Mapped[time] = mapped_column(Time, nullable=False)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(onupdate=func.now(), nullable=True)
    booking: Mapped["Booking"] = relationship("Booking", back_populates="showtime")

    movies: Mapped[Movie] = relationship(Movie, backref="showtime")
    theatre_halls: Mapped[List[TheatreHall]] = relationship(
        TheatreHall, back_populates="showtime"
    )

    __table_args__ = (
        CheckConstraint("price >= 0", name="check_price_is_non_negative"),
    )


class BookingStatus(str, Enum):
    CANCELED = "CANCELED"
    SOLD = "SOLD"
    PENDING = "PENDING"


class Booking(Base):
    __tablename__ = "booking"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    u_id: Mapped[str] = mapped_column(
        String(100), default=lambda: generate(), unique=True
    )
    booking_status: Mapped[str] = mapped_column(
        String(8), nullable=False, default=BookingStatus.PENDING
    )
    showtime_id: Mapped[int] = mapped_column(ForeignKey("show_time.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    theatre_hall_id: Mapped[int] = mapped_column(ForeignKey("theatre_halls.id"))
    added_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )
    user: Mapped[List[User]] = relationship(User, backref="booking")
    theatre_halls: Mapped[TheatreHall] = relationship(
        TheatreHall, back_populates="booking"
    )
    seats: Mapped[List[Seat]] = relationship(
        secondary=booking_seats, back_populates="booking"
    )
    showtime: Mapped[ShowTime] = relationship(ShowTime, back_populates="booking")
    ticket: Mapped["Ticket"] = relationship("Ticket", back_populates="booking")


class Ticket(Base):
    __tablename__ = "ticket"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    issued_at: Mapped[datetime] = mapped_column(onupdate=func.now(), nullable=True)
    expires_at: Mapped[datetime]
    token: Mapped[str] = mapped_column(String(200), nullable=True)
    booking_id: Mapped[int] = mapped_column(ForeignKey("booking.id"), nullable=True)

    booking: Mapped[Booking] = relationship(Booking, back_populates="ticket")


class SeatBooked(Base):
    __tablename__ = "seat_booked"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # row_name: Mapped[str] = mapped_column(String(1), nullable=True)
    available_seats: Mapped[int] = mapped_column(nullable=True)
    # total_seats: Mapped[int]
    theatrehall_id: Mapped[int] = mapped_column(ForeignKey("theatre_halls.id"))
    added_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(onupdate=func.now(), nullable=True)

    theatre_halls: Mapped[TheatreHall] = relationship(
        TheatreHall, back_populates="seat_booked"
    )

    __table_args__ = (
        CheckConstraint(
            "available_seats >= 0", name="check_available_seats_non_negative"
        ),
    )
