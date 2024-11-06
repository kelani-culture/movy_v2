from datetime import date, time
from decimal import Decimal
from typing import List

from pydantic import BaseModel, ConfigDict, computed_field


class Genre(BaseModel):
    id: int
    name: str


class MovieStream(BaseModel):
    u_id: str
    title: str
    tagline: str | None = None
    status: str
    poster_path: str
    genres: List[Genre]

    @computed_field
    def movie_path(self) -> str:
        return f"/movie/{self.u_id}"

    model_config = ConfigDict(from_attributes=True)


class Seat(BaseModel):
    row_name: str
    seat: int
    status: str


class AvailableSeat(BaseModel):
    available_seats: int


class TheatreHall(BaseModel):
    id: int
    seat_booked: AvailableSeat
    name: str
    seats: List[Seat]


class ShowTime(BaseModel):
    u_id: str
    stream_date: date
    start_time: time
    end_time: time
    theatre_halls: TheatreHall


class MovieDetailStream(BaseModel):
    u_id: str
    title: str
    tagline: str | None = None
    summary: str | None = None
    status: str
    poster_path: str
    backdrop_path: str
    genres: List[Genre]

    showtime: List[ShowTime]

class ShowTime(BaseModel):
    u_id: str
    stream_date: date
    start_time: time
    end_time: time
    price: Decimal

class Theatrehall(BaseModel):
    id: int
    name: str

class BookingDetail(BaseModel):
    u_id: str
    booking_status: str
    theatre_halls: Theatrehall 
    showtime: ShowTime
    seats: List[Seat]
