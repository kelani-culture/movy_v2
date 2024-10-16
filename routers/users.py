from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from database import get_db
from models.user_model import User
from schemas.user_schema import (
    ProfilePicResponse,
    UserLoginSchema,
    UserResponseLoginSchema,
    UserResponseSchema,
    UserSignUpSchema,
)
from services.auth import (
    create_user,
    get_current_user_or_theatre,
    update_profile_pic,
    user_login,
)

routers = APIRouter(prefix="/user/auth", tags=["User Auth"])

profile = APIRouter(prefix="/user", tags=["User Profile"])


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


@profile.patch("/upload-profile-image", status_code=200)
async def profile_picture(
    pic: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user_or_theatre),
) -> ProfilePicResponse:
    """
    user profile picture upload
    """
    profile = update_profile_pic(db, pic, user)

    return ProfilePicResponse(
        profile_path=profile, message="User upload successful", status_code=200
    )


# TODO delete routes after testing if endpoint is protected
@routers.get("/protected-route-motherfucker")
def protected(user=Depends(get_current_user_or_theatre)):
    return "It's bloody protected y'all"
