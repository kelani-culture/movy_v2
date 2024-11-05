from typing import List

from fastapi import APIRouter, Depends, Request, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from database import get_db
from models.movie_model import MovieStatus
from schemas.showtime_schema import MovieDetailStream, MovieStream
from services.manager import ConnectionManager, handle_user_booking
from services.showtime import movie_info, stream_movies

routers = APIRouter(prefix="/movies", tags=["Movies"])


manager = ConnectionManager()


@routers.get("/", response_model=List[MovieStream], status_code=200)
def movie_streaming(request: Request, db: Session = Depends(get_db)):
    """
    movie stream routes
    """
    return stream_movies(db, MovieStatus.RELEASED)


@routers.get("/upcoming", response_model=List[MovieStream], status_code=200)
def upcoming_movies(db: Session = Depends(get_db)):
    """
    upcoming movies
    """
    return stream_movies(db, MovieStatus.UPCOMING)


@routers.get("/{movie_id}", response_model=MovieDetailStream)
def movie_detail(movie_id: str, db: Session = Depends(get_db)):
    """
    movie details
    """
    return movie_info(db, movie_id)


@routers.websocket("/book/{showtime_id}")
async def booking(
    websocket: WebSocket,
    showtime_id: str,
    db: Session = Depends(get_db),
):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            seat_update = await handle_user_booking(websocket, db, showtime_id, data)
            await manager.seat_booking(seat_update)
    except ValueError:
        await websocket.send_json({"error": "Invalid Json body parsed"})
        # await websocket.close(close=1008)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
