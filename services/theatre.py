from datetime import date, datetime
from typing import Dict, List

from sqlalchemy.orm import Session

from models.theatre_model import Address, Theatre, TheatreHall
from models.movie_model import Movie, Genre
from utils.create_seats import generate_theatre_seats
from utils.handle_image import image_upload
from schemas.settings import STATIC_DIRECTORY

def create_theatre_address(
    db: Session, data: Dict[str, str], theatre: Theatre
) -> Theatre:
    """
    handles user theatre address creation
    """
    description = data.pop("description")
    address = Address(**data)
    db.add(address)

    theatre.description = description
    theatre.addresses.append(address)
    db.commit()

    db.refresh(theatre)

    return theatre


def create_theatre_halls_seats(
    db: Session, data: Dict[str, int | str], theatre: Theatre
) -> None:
    """
    create user theatre halls and seats
    """
    theatre_hall = TheatreHall(**data)
    db.add(theatre_hall)

    theatre.theatre_halls.append(theatre_hall)

    total_row = data["total_row"]
    seats_per_row = data["seats_per_row"]
    seats = generate_theatre_seats(db, total_row, seats_per_row)

    theatre_hall.seats.extend(seats)
    db.add_all(seats)
    db.commit()


def get_theatre_detail(db: Session, theatre: Theatre) -> Theatre:
    """
    get all full detail on theatre
    """
    return db.query(Theatre).filter(Theatre.id == theatre.id).first()



def theatre_create_movie(db: Session, theatre, **kwargs) -> None:
    """
    handles theatre create movie
    """

    movie_dir = STATIC_DIRECTORY / "movies" / f"{datetime.date(datetime.now())}"

    backdrop_path = image_upload(movie_dir, kwargs.pop("backdrop_path"))
    poster_path = image_upload(movie_dir, kwargs.pop("poster_path"))

    genres = kwargs.pop("genres")
    kwargs["status"] = kwargs["status"].upper()
    n_genre = []
    for gen in genres:
        genre = db.query(Genre).filter(Genre.name == gen).first()

        if not genre:
            genre = Genre(name=gen)
            db.add(genre)
        n_genre.append(genre)
        
    movie = Movie(**kwargs)
    movie.backdrop_path = backdrop_path
    movie.poster_path = poster_path
    movie.genres.extend(n_genre)
    db.add(movie)
    db.commit()



def all_movies(db: Session) -> List[Movie]:
    """
    return all movies
    """
    return db.query(Movie).all()
