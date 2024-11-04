from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.movie_model import Movie, MovieStatus
from models.theatre_model import ShowTime


def stream_movies(db: Session, status: MovieStatus) -> Movie:
    s = (
        select(Movie, ShowTime)
        .join(ShowTime, ShowTime.movie_id == Movie.id)
        .where(Movie.status == status, datetime.now().date() < ShowTime.stream_date)
    )
    return db.execute(s).scalars().all()


def movie_info(db: Session, u_id: str) -> Movie:
    return db.query(Movie).filter(Movie.u_id == u_id).first()
