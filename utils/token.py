import datetime
from datetime import datetime, timedelta
from typing import Dict

import jwt

from models.theatre_model import Theatre
from models.user_model import User
from schemas.settings import setting

setting = setting()

ALGORITHM = "HS256"


def create_user_token(
    data: Dict[str, str],
    secret_key: str,
    expires_at: timedelta | None,
) -> str:
    """
    create user jwt token
    """

    if not expires_at:
        data["exp"] = datetime.now() + timedelta(minutes=5)
    else:
        data["exp"] = datetime.now() + timedelta(minutes=expires_at)

    data["iss"] = "http://localhost:8000" #FIXME change to production domain....
    data["iat"] = datetime.now()
    data["aud"] = "movy-app-api"
    return jwt.encode(payload=data, key=secret_key, algorithm=ALGORITHM)


def generate_user_token(user: User | Theatre, type_user: str) -> Dict[str, str | int]:
    """
    Handle user token generation...
    """

    if isinstance(user, Theatre):
        name = user.name

    if isinstance(user, User):
        name = f"{user.last_name} {user.first_name}"

    access_token_data = {
        "name": name,
        "user_id": user.id,
        "sub": user.u_id,
        "email": user.email,
        "email_verified": user.is_verified,
        "sign_in_provider": user.provider.value,
    }

    access_token = create_user_token(
        access_token_data,
        setting.access_token_secret_key,
        setting.ACCESS_TOKEN_EXPIRE_MIN,
    )

    refresh_token_data = {"sub": user.u_id, "email": user.email}
    refresh_token = create_user_token(
        refresh_token_data,
        setting.refresh_token_secret_key,
        setting.REFRESH_TOKEN_EXPIRE_MIN,
    )

    expires_at = int(timedelta(minutes=setting.ACCESS_TOKEN_EXPIRE_MIN).total_seconds())
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "expires_at": expires_at,
    }
