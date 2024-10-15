from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas.user_schema import (
    UserLoginSchema,
    UserResponseLoginSchema,
    UserResponseSchema,
    UserSignUpSchema,
)
from services.auth import create_user, get_current_user_or_theatre, user_login

routers = APIRouter(prefix="/user/auth", tags=["User Auth"])


@routers.post("/signup", response_model=UserResponseSchema, status_code=201)
def signup(user: UserSignUpSchema, db: Session = Depends(get_db)) -> UserResponseSchema:
    """
    user signup routes
    """
    create_user(db, **user.model_dump())
    return UserResponseSchema(message="User created successfully", status_code=201)


@routers.post("/login", response_model=UserResponseLoginSchema)
async def login(user: UserLoginSchema, db: Session = Depends(get_db)):
    """
    user login routes
    """
    info = await user_login(db, **user.model_dump())
    return UserResponseLoginSchema(**info)


#TODO delete routes after testing if endpoint is protected
@routers.get("/protected-route-motherfucker")
def protected(user=Depends(get_current_user_or_theatre)):
    return ("It's bloody protected y'all")
