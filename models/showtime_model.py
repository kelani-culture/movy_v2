from datetime import date, datetime
from time import time
from typing import List

from nanoid import generate
from sqlalchemy import ForeignKey, String, func, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from models.theatre_model import TheatreHall

from .movie_model import Movie


class ShowTime(Base):
    __tablename__ = "show_time"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    u_id: Mapped[str] = mapped_column(String(100), default=lambda: generate(), unique=True)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"))
    theatre_hall_id: Mapped[int] = mapped_column(ForeignKey("theatre_halls.id"))
    stream_date: Mapped[date] = mapped_column(nullable=False)
    start_time: Mapped[time] = mapped_column(Time, nullable=False)
    end_time: Mapped[time] = mapped_column(Time, nullable=False)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(onupdate=True)

    movies: Mapped[List[Movie]] = relationship(Movie, back_populates="showtime")
    theatre_halls: Mapped[List[TheatreHall]] = relationship(TheatreHall, back_populates="showtime")

