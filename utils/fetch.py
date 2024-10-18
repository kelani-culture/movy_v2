#!/usr/bin/env python3
from sys import exit
from typing import Dict

import httpx
from sqlalchemy.exc import IntegrityError

from database import Session
from models.movie_model import Genre, Movie
from schemas.settings import setting

setting = setting()


def _send_request(
    url: str, params: Dict[str, str], header: Dict[str, str]
) -> Dict[str, str | int]:
    """
    send user request to tmdb api
    """
    try:
        with httpx.Client() as client:
            resp = client.get(url=url, params=params, headers=header)
    except (httpx.RequestError, httpx.TimeoutException) as e:
        print("enve")
        print(e)
        exit(1)
    return resp.json()


class TMDB:
    def __init__(self):
        self.header = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {setting.tmdb_access_token}",
        }
        self.params = {"api_key": setting.tmdb_api_key}
        self.url = "https://api.themoviedb.org/3"
        self.movie_id = []

    def get_movie_genre(self):
        """
        get each movie genres
        """
        url = f"{self.url}/genre/movie/list?language=en"

        genres = _send_request(url, self.params, self.header)["genres"]

        for genre in genres:
            try:
                with Session() as session:
                    with session.begin():
                        genre = Genre(name=genre["name"])
                        session.add(genre)
                        session.commit()
            except IntegrityError:
                continue

    def get_popular_movies(self, count=1):
        """
        get movies popularity
        """

        # for i in range(1, 4):
        #     url = f"{self.url}/movie/popular?language=en-US&page={i}"
        #     movies = _send_request(url, self.params, self.header)["results"]

        if count > 4:
            return

        url = f"{self.url}/movie/popular?language=en-US&page={count}"  # increment movie page

        resp = _send_request(url, self.params, header=self.header)["results"]

        # get movie detailed from tmdb
        for movie in resp:
            poster_path = f"https://image.tmdb.org/t/p/original{movie['poster_path']}"
            backdrop_path = (
                f"https://image.tmdb.org/t/p/original{movie['backdrop_path']}"
            )

            t_url = f"{self.url}/movie/{movie['id']}/videos?language=en-US"

            # get movie trailer link
            get_trailer = _send_request(t_url, self.params, self.header)["results"]

            trailer_link = None
            for trailer in get_trailer:
                if (
                    trailer["type"] == "Official"
                    or trailer["name"] == "Official Teaser"
                    or trailer["type"] == "Clip"
                ):
                    trailer_link = f"https://www.youtube.com/watch?v={trailer['key']}"

            d_url = (
                f"{self.url}/movie/{movie['id']}?language=en-US"  # fetch movie detail
            )
            movie_d = _send_request(d_url, self.params, self.header)
            # add movie to the Movie table

            if (
                movie_d["status"].lower() != "released"
                and movie_d["status"].lower() != "upcoming"
            ):
                continue

            with Session() as session:
                with session.begin():
                    detail = {
                        "title": movie_d["title"],
                        "summary": movie_d["overview"],
                        "poster_path": poster_path,
                        "backdrop_path": backdrop_path,
                        "trailer_link": trailer_link,
                        "release_date": movie_d["release_date"],
                        "duration_in_min": movie_d["runtime"],
                        "tagline": movie_d["tagline"],
                        "status": movie_d["status"].lower(),
                    }
                movie_obj = Movie(**detail)
                session.add(movie_obj)
                for genre in movie_d["genres"]:
                    q = session.query(Genre).filter(Genre.name == genre["name"]).one_or_none()
                    if not q:
                        continue
                    movie_obj.genres.append(q)
                # self.movie_id.append((movie["id"], movie.id)) # append both movie id and movie obj to movie_id list
                session.commit()
        self.get_popular_movies(count + 1)


if __name__ == "__main__":
    tmdb = TMDB()
    # tmdb.get_movie_genre()
    tmdb.get_popular_movies()
