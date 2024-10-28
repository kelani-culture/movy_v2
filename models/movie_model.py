from datetime import date, datetime
from enum import Enum
from typing import List

from nanoid import generate
from sqlalchemy import Column, DateTime, ForeignKey, Index, String, Table, Text, func
from sqlalchemy import Enum as SQLALCHEMY_ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

movie_genres = Table(
    "movie_genres",
    Base.metadata,
    Column("genre_id", ForeignKey("genres.id"), nullable=False),
    Column("movie_id", ForeignKey("movies.id"), nullable=False),
)

# movie_casts = Table(
#     "movie_casts",
#     Base.metadata,
#     Column("cast_id", ForeignKey("casts.id")),
#     Column("movie_id", ForeignKey("movies.id")),
# )

# movie_directors = Table(
#     "movie_directors",
#     Base.metadata,
#     Column("director_id", ForeignKey("directors.id")),
#     Column("movie_id", ForeignKey("movies.id")),
# )


class MovieStatus(Enum):
    RELEASED = "released"
    UPCOMING = "upcoming"


class Movie(Base):
    __tablename__ = "movies"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    u_id: Mapped[str] = mapped_column(
        String(100), default=lambda: generate(), unique=True, nullable=False
    )
    title: Mapped[str] = mapped_column(String(100), index=True)
    tagline: Mapped[str] = mapped_column(String(200), nullable=True, index=True)
    summary: Mapped[str] = mapped_column(Text, nullable=True, index=True)
    trailer_link: Mapped[str] = mapped_column(String(100), nullable=True)
    duration_in_min: Mapped[str] = mapped_column(String(200))
    release_date: Mapped[date] = mapped_column(index=True)
    poster_path: Mapped[str] = mapped_column(String(100), nullable=True)
    backdrop_path: Mapped[str] = mapped_column(String(100), nullable=True)
    added_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )

    status: Mapped[Enum] = mapped_column(
        SQLALCHEMY_ENUM(MovieStatus), nullable=False, index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, onupdate=func.now(), nullable=True
    )
    # casts: Mapped[List["Cast"]] = relationship(
    #     secondary=movie_casts, back_populates="movies"
    # )
    genres: Mapped[List["Genre"]] = relationship(
        secondary=movie_genres, back_populates="movies"
    )
    # directors: Mapped[List["Director"]] = relationship(
    #     secondary=movie_directors, back_populates="movies"
    # )

    def __str__(self):
        return self.title

    __table_args__ = (
        Index(
            "ix_movies_summary", "summary", mysql_length=255
        ),  # specify key length for MySQL
    )


class Cast(Base):
    __tablename__ = "casts"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), index=True)
    profile_path: Mapped[str] = mapped_column(String(100), nullable=True)

    # movies: Mapped[List[Movie]] = relationship(
    #     secondary=movie_casts, back_populates="casts"
    # )

    def __str__(self):
        return self.name


class Director(Base):
    __tablename__ = "directors"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), index=True)
    profile_path: Mapped[str] = mapped_column(String(100), nullable=True)
    # movies: Mapped[List[Movie]] = relationship(
    #     secondary=movie_directors, back_populates="directors"
    # )

    def __str__(self):
        return self.name


class Genre(Base):
    __tablename__ = "genres"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(20), unique=True)
    movies: Mapped[List[Movie]] = relationship(
        secondary=movie_genres, back_populates="genres"
    )

    def __str__(self):
        return self.name
