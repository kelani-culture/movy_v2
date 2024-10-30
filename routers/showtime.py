from typing import List
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from database import get_db
from schemas.showtime_schema import MovieStream
from services.showtime import stream_movies

routers = APIRouter(prefix="/movies")




@routers.get("/", response_model=List[MovieStream], status_code=200)
def movie_streaming(request: Request, db: Session = Depends(get_db)):
    """
    movie stream routes
    """
    return stream_movies(db)