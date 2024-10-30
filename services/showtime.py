from sqlalchemy.orm import Session
from models.movie_model import Movie


def stream_movies(db: Session):
    return db.query(Movie).all()