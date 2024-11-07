from typing import List

from fastapi import APIRouter, Depends, Request, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from database import get_db
from models.movie_model import MovieStatus
from models.user_model import User
from schemas.showtime_schema import BookingDetail, MovieDetailStream, MovieStream
from services.auth import get_user
from services.manager import ConnectionManager, handle_user_booking
from services.showtime import get_user_booking, movie_info, stream_movies

routers = APIRouter(prefix="/movies", tags=["Movies"])
booking_route = APIRouter(prefix="/booking", tags=["Book Movie"])

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


@booking_route.get("/", response_model=BookingDetail)
def get_all_booking(db: Session = Depends(get_db), user: User = Depends(get_user)):
    """
    handle booking routes
    """
    return get_user_booking(db, user)


@booking_route.websocket("/{showtime_id}")
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


@booking_route.websocket("/cancel/{booking_id}")
async def cancel_user_booking(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        # await manager.
        ...
    except WebSocketDisconnect:
        ...
