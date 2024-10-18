from datetime import datetime, timedelta
from typing import Dict

import jwt
from dateutil import tz
from jwt.exceptions import InvalidAudienceError, InvalidTokenError

# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from exception import AccountDisabled, InvalidAccessTokenProvided
from models.theatre_model import Theatre
from models.user_model import User
from schemas.settings import setting
from schemas.user_schema import TokenPayload

setting = setting()

ALGORITHM = "HS256"
EXPECTED_AUDIENCE = "movy-app-api"


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

    return jwt.encode(payload=data, key=secret_key, algorithm=ALGORITHM)


def generate_user_token(user: User | Theatre, type_user: str) -> Dict[str, str | int]:
    """
    Handle user token generation...
    """

    if isinstance(user, Theatre):
        name = user.name

    if isinstance(user, User):
        name = f"{user.last_name} {user.first_name}"

    role = (
        "user"
        if type_user == "user"
        else "theatre"
        if type_user == "theatre"
        else "admin",
    )
    gmt = tz.gettz("GMT")
    access_token_data = {
        "iss": "http://localhost:8000",
        "iat": int(datetime.now(tz=gmt).timestamp()),
        "aud": "movy-app-api",
        "user": {
            "name": name,
            "user_id": user.id,
            "sub": user.u_id,
            "email": user.email,
            "role": role,
        },
        "is_active": user.is_active,
        "email_verified": user.is_verified,
        "sign_in_provider": user.provider.value,
    }

    access_token = create_user_token(
        access_token_data,
        setting.access_token_secret_key,
        setting.ACCESS_TOKEN_EXPIRE_MIN,
    )
    refresh_token_data = {
        "iss": "http://localhost:8000",
        "iat": int(datetime.now(tz=gmt).timestamp()),
        "aud": EXPECTED_AUDIENCE,
        "sub": user.u_id,
    }
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


def decode_user_token(token: str) -> TokenPayload:
    """
    decode user token from the payload...
    """
    try:
        payload = jwt.decode(
            token,
            setting.access_token_secret_key,
            algorithms=[ALGORITHM],
            audience=EXPECTED_AUDIENCE,
        )
        user_info = payload.get("user", {})
        if not user_info:
            print(user_info)
            raise InvalidAccessTokenProvided("Invalid token provided or token expired")

        if not payload.get("is_active"):
            print("user_info")
            raise AccountDisabled("User account has been disabled please contact admin")

        user = TokenPayload(**user_info)
    except (InvalidTokenError, InvalidAudienceError) as e:
        print(e)
        raise InvalidAccessTokenProvided("Invalid token provided or token expired")

    return user
