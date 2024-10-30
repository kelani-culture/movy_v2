from typing import List

from fastapi import Request
from pydantic import BaseModel, ConfigDict, HttpUrl, computed_field


class Genre(BaseModel):
    id: int
    name: str


class MovieStream(BaseModel):
    u_id: str
    title: str
    tagline: str
    poster_path: str
    genres: List[Genre]

    @computed_field
    def movie_path(self) -> str:
        return f"/movie/{self.u_id}"

    model_config = ConfigDict(from_attributes=True)
