from datetime import date
from typing import Annotated, List

from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from fastapi.responses import JSONResponse
from pydantic import HttpUrl
from sqlalchemy.orm import Session

from database import get_db
from models.theatre_model import Theatre
from schemas.theatre_schema import (
    TheatreAddressSchema,
    TheatreHall,
    TheatreInfo,
    TheatreMovie,
    TheatreResponse,
    TheatreShowTime,
)
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
from services.theatre import (
    all_movies,
    create_theatre_address,
    create_theatre_halls_seats,
    get_theatre_detail,
    show_time_theatre,
    theatre_create_movie,
)

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


# @profile_routers.post(
#     "/movie"
# )
# def theatre_movie_streams():
#     ...


@profile_routers.post(
    "/theatre-hall/create", response_model=TheatreResponse, status_code=201
)
def create_theatre_hall(
    data: TheatreHall,
    db: Session = Depends(get_db),
    theatre: Theatre = Depends(get_current_user_or_theatre),
):
    """
    create theatre movie hall including seats
    """
    create_theatre_halls_seats(db, data.model_dump(), theatre)
    message = {"message": "Theatre created successful", "status_code": 201}
    return JSONResponse(content=message, status_code=status.HTTP_201_CREATED)


@profile_routers.get("/theatre-info", response_model=TheatreInfo)
def get_theatre_info(
    db: Session = Depends(get_db),
    theatre: Theatre = Depends(get_current_user_or_theatre),
):
    """
    get all info about a theatre
    """
    theatre = get_theatre_detail(db, theatre)
    return theatre


@profile_routers.post("/create-movie", status_code=201)
def create_movie(
    title: Annotated[str, Form(...)],
    summary: Annotated[str | None, Form(...)],
    status: Annotated[str, Form(...)],
    duration_in_min: Annotated[int, Form(...)],
    genres: Annotated[List[str], Form(...)],
    trailer_link: Annotated[HttpUrl, Form(...)],
    tagline: Annotated[str | None, Form(...)],
    release_date: Annotated[date, Form(...)],
    poster_path: Annotated[UploadFile, Form(...)],
    backdrop_path: Annotated[UploadFile, Form(...)],
    db: Session = Depends(get_db),
    theatre: Theatre = Depends(get_current_user_or_theatre),
):
    """
    create theatre movie routes
    """
    theatre_create_movie(
        db,
        theatre,
        title=title,
        summary=summary,
        duration_in_min=duration_in_min,
        genres=genres,
        trailer_link=trailer_link,
        tagline=tagline,
        release_date=release_date,
        poster_path=poster_path,
        backdrop_path=backdrop_path,
        status=status,
    )

    return {"message": "Movie added successfully", "status_code": 201}


@profile_routers.get("/all-movies", response_model=List[TheatreMovie])
def get_all_movies(
    db: Session = Depends(get_db),
    theatre: Theatre = Depends(get_current_user_or_theatre),
):
    """
    get all movies uploaded
    """
    return all_movies(db)


# TODO  write both the update and delete endpoint for theatre movies
# @profile_routers.patch("/update-movies")
# def update_movies(

#     db: Session, theatre: Theatre = Depends(get_current_user_or_theatre)):
#     """
#     update movie info
#     """
#     return all_movies(db)


@profile_routers.post("/create-showtime", status_code=201)
def create_theatre_show_time(
    show: TheatreShowTime,
    db: Session = Depends(get_db),
    theatre: Theatre = Depends(get_current_user_or_theatre),
):
    """
    showtime routes
    """
    show_time_theatre(db, show.model_dump())
    return JSONResponse(
        content={"message": "Theatre show time added successfully"}, status_code=201
    )
