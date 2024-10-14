from pydantic import BaseModel, EmailStr



class UserSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr



class UserSignUpSchema(UserSchema):
    password: str


class UserResponseSchema(BaseModel):
    message: str
    status_code: int

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class UserResponseLoginSchema(BaseModel):
    full_name: str
    email: EmailStr
    profile_pic: str | None
    access_token: str
    refresh_token: str
    expires_at: int

    # model_config = {
    #     "from_attributes": True
    # }
