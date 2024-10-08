from fastapi import APIRouter

routers = APIRouter(prefix="/auth")


#TODO Implement user auth...
@routers.post("/signup")
def signup():
    ...