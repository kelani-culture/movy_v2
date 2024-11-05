from typing import Dict, List

from fastapi.websockets import WebSocket
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from exception import InvalidAccessTokenProvided
from models.theatre_model import (
    Booking,
    Seat,
    SeatBooked,
    SeatStatus,
    ShowTime,
    TheatreHall,
)
from models.user_model import User
from utils.jwt_token import decode_user_token


async def handle_websocket_token(
    db: Session, websocket: WebSocket, token: str | None = None
):
    """
    websocket token
    """
    user_info = None
    try:
        user_info = decode_user_token(token)
        user = db.query(User).filter(User.email == user_info.email).first()

        if not user:
            await websocket.send_json({"error": "User cannot reserve seats"})
            await websocket.close(code=1008)
        return user
    except InvalidAccessTokenProvided:
        await websocket.send_json({"error": "Invalid token provided"})
        await websocket.close(code=1008)


class ConnectionManager:
    def __init__(self):
        self.connected_clients: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connected_clients.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        self.connected_clients.remove(websocket)

    async def seat_booking(self, message: Dict[str, str | int]):
        """
        book user seats...
        """
        for connection in self.connected_clients:
            await connection.send_json(message)


async def handle_user_booking(
    websocket: WebSocket, db: Session, showtime_id: str, data: Dict[str, List[int]]
) -> Dict[str, str | List[int]]:
    token = websocket.headers.get("Authorization")
    user = await handle_websocket_token(db, websocket, token)
    showtime = db.query(ShowTime).filter(ShowTime.u_id == showtime_id).first()
    if not showtime:
        await websocket.send_json({"error": "ShowTime  cannot be found"})

    # create booking
    try:
        hall_id = data.pop("theatrehall_id")
        theatrehall = db.query(TheatreHall).filter(TheatreHall.id == hall_id).first()

        if not theatrehall:
            await websocket.send_json({"error": "Theatre Hall does not exists"})
            await websocket.close(code=1008)
        seats = data["seats"][0]

        all_seat = []

        for k in seats:  # check for seats availability
            query = (
                db.query(Seat)
                .filter(
                    and_(
                        Seat.row_name == k,
                        Seat.seat.in_(seats[k]),
                        Seat.theatre_hall_id == hall_id,
                    )
                )
                .all()
            )
            for seat in query:
                if (
                    seat.status == SeatStatus.RESERVED
                    or seat.status == SeatStatus.BOOKED
                ):
                    await websocket.send_json(
                        {
                            "error": "Seat not available for Booking",
                            "unavailable_seat": {
                                "row_name": seat.row_name,
                                "seat": seat.seat,
                            },
                        }
                    )
                    websocket.close(code=1008)
                else:
                    # seat_booked = SeatBooked()
                    seat.status = SeatStatus.RESERVED
                    all_seat.extend(query)

        seat_booked = (
            db.query(SeatBooked).filter(SeatBooked.theatrehall_id == hall_id).first()
        )

        if not seat_booked:
            print("seat not booked")
            pass
        else:
            seat_booked.available_seats -= len(all_seat)
        booking = Booking()
        booking.showtime = showtime
        booking.user = user
        booking.seats.extend(all_seat)
        booking.theatre_halls = theatrehall
        db.add(booking)
        db.commit()
    except IntegrityError as e:
        print(e)
        await websocket.send_json({"error": str(e)})
        # await websocket.close(code=1008)
        db.rollback()
    data = [
        {
            "available_seats": seat_booked.available_seats,
            "row_name": seat.row_name,
            "seat": seat.status,
            "status": seat.status,
        }
        for seat in all_seat
    ]
    return data
