from typing import Annotated

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from database import get_db
from models.theatre_model import Theatre
from schemas.theatre_schema import TheatreResponse, TheatreAddressSchema
from schemas.user_schema import (
    ProfilePicResponse,
    TheatreResponseLoginSchema,
    TheatreSignUpSchema,
    UserLoginSchema,
    UserResponseSchema,
)
from services.auth import (
    create_user,
    get_current_user_or_theatre,
    update_profile_pic,
    user_login,
)
from services.theatre import create_theatre_address

routers = APIRouter(prefix="/theatre/auth", tags=["Theatre Auth"])

profile_routers = APIRouter(prefix="/theatre", tags=["Theatre Profile"])


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


@profile_routers.patch("/upload-profile-image", response_model=ProfilePicResponse)
async def theatre_profile_image_upload(
    pic: Annotated[UploadFile, File(...)],
    db: Session = Depends(get_db),
    theatre: Theatre = Depends(get_current_user_or_theatre),
) -> ProfilePicResponse:
    """
    theatre profile image route
    """
    profile_path = update_profile_pic(db, pic, theatre, "theatre")
    return ProfilePicResponse(
        profile_path=profile_path,
        message="Theatre profile update successfully",
        status_code=200,
    )


@profile_routers.post(
    "/theatre-address", response_model=TheatreResponse, status_code=201
)
def theatre_address(
    data: TheatreAddressSchema,
    db: Session = Depends(get_db),
    theatre: Theatre = Depends(get_current_user_or_theatre),
):
    theatre = create_theatre_address(db, data.model_dump(), theatre)
    return theatre
