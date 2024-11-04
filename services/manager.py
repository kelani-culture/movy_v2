from typing import List

from fastapi.websockets import WebSocket
from sqlalchemy.orm import Session

from exception import InvalidAccessTokenProvided, PermissionNotAllowed
from models.user_model import User
from utils.jwt_token import decode_user_token


async def handle_websocket_token(
    db: Session, websocket: WebSocket, token: str | None = None
):
    """
    websocket token
    """
    try:
        user_info = decode_user_token(token)
    except InvalidAccessTokenProvided:
        await websocket.send_json({"error": "Invalid token provided"})
        await websocket.close(code=1008)

    user = db.query(User).filter(User.email == user_info.email).first()

    if not user:
        await websocket.send_json({"error": "User cannot reserve seats"})
        await websocket.close(code=1008)
    return user


class ConnectionManager:
    def __init__(self):
        self.connected_clients: List[WebSocket] = []

    async def connect(self, websocket: WebSocket, db: Session):
        await websocket.accept()
        self.connected_clients.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        self.connected_clients.remove(websocket)
        print(self.connected_clients)

    async def seat_booking(self, websocket: WebSocket, db: Session, showtime_id: str):
        token = websocket.headers.get("Authorization")
        user = await handle_websocket_token(db, websocket, token)
        message = {"client": "Yay"}
        await websocket.send_json(message)
