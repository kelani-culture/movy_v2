from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from exception import BookingMissingException, MovieException
from models.movie_model import Movie, MovieStatus
from models.theatre_model import Booking, ShowTime
from models.user_model import User


def stream_movies(db: Session, status: MovieStatus) -> Movie:
    s = (
        select(Movie, ShowTime)
        .join(ShowTime, ShowTime.movie_id == Movie.id)
        .where(Movie.status == status, datetime.now().date() < ShowTime.stream_date)
    )
    return db.execute(s).scalars().all()


def movie_info(db: Session, u_id: str) -> Movie:
    movie = db.query(Movie).filter(Movie.u_id == u_id).first()
    if not movie:
        raise MovieException("Movie not found")
    return movie


def get_user_booking(db: Session, user: User) -> Booking:
    booking = db.query(Booking).filter(Booking.user_id == user.id).first()
    if booking is None:
        raise BookingMissingException("Booking not found")

    return booking
