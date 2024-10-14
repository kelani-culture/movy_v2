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
    emaiL: str
    password: str


class UserResponseLoginSchema(UserSchema):
    profile_pic: str | None

    model_config = {
        "from_attributes": True
    }
