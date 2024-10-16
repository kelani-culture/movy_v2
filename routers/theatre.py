from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas.user_schema import (
    TheatreResponseLoginSchema,
    TheatreSignUpSchema,
    UserLoginSchema,
    UserResponseSchema,
)
from services.auth import create_user, user_login

routers = APIRouter(prefix="/theatre/auth", tags=["THEATRE Auth"])


@routers.post("/signup", response_model=UserResponseSchema, status_code=201)
async def theatre_signup(theatre: TheatreSignUpSchema, db: Session = Depends(get_db)):
    """
    theatre login route
    """
    create_user(db, "theatre", **theatre.model_dump())
    return UserResponseSchema(message="Theatre created successfully", status_code=201)


@routers.post("/login", response_model=TheatreResponseLoginSchema)
async def theatre_login(theatre: UserLoginSchema, db: Session = Depends(get_db)):
    """
    theatre login route
    """
    theatre = await user_login(db, "theatre", **theatre.model_dump())
    return TheatreResponseLoginSchema(**theatre)
