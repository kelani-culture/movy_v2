import pytest
from faker import Faker

from models.user_model import User


@pytest.fixture()
def user():
    faker = Faker()
    return {
        "first_name": faker.first_name(),
        "last_name": faker.last_name(),
        "email": faker.email(safe=True),
        "password": faker.password(length=8, special_chars=True, upper_case=True),
    }


class TestUserAuth:
    def test_create_user_successful(self, client, user):
        url = "/user/auth/signup"
        resp = client.post(url, json=user)
        assert resp.status_code == 201
        assert resp.json() == {
            "message": "User created successfully",
            "status_code": 201,
        }

    def test_create_user_unsuccessful(self, client, db_session, user):
        user_d = User(**user)
        db_session.add(user_d)
        db_session.commit()

        url = "/user/auth/signup"
        resp = client.post(url, json=user)
        resp_msg = {"message": "User email already exists please proceed to login"}
        assert resp.status_code == 400
        assert resp.json() == resp_msg

    def test_user_login(self, client, user, db_session):
        user_d = User(**user)
        user_d.is_verified = True
        db_session.add(user_d)
        db_session.commit()

        url = "/user/auth/login"
        user = {"email": user["email"], "password": user["password"]}
        resp = client.post(url, json=user)
        print(resp.json())
        assert resp.status_code == 200
        assert "access_token" in resp.json()
        assert "refresh_token" in resp.json()
        assert "full_name" in resp.json()
        assert "profile_pic" in resp.json()
        assert "expires_at" in resp.json()

    def test_user_email_not_verified(self, client, user, db_session):
        user_d = User(**user)
        db_session.add(user_d)
        db_session.commit()

        url = "/user/auth/login"
        user = {"email": user["email"], "password": user["password"]}
        resp = client.post(url, json=user)
        assert resp.status_code == 400
        assert resp.json() == {
            "message": "Your account has not been verified please check your inbox"
        }

    def test_user_invalid_email(self, client, user):
        url = "/user/auth/login"
        user = {"email": user["email"], "password": user["password"]}
        resp = client.post(url, json=user)
        assert resp.status_code == 400
        assert resp.json() == {"message": "Invalid email or password provided"}

    def test_user_account_disabled(self, client, user, db_session):
        user_d = User(**user)
        user_d.is_active = False
        db_session.add(user_d)
        db_session.commit()

        url = "/user/auth/login"
        user = {"email": user["email"], "password": user["password"]}
        resp = client.post(url, json=user)
        assert resp.status_code == 400
        assert resp.json() == {
            "message": "Your account has been disabled please contact admin"
        }

    def test_user_account_not_verified(self, client, user, db_session):
        user_d = User(**user)
        user_d.is_verified = False
        db_session.add(user_d)
        db_session.commit()

        url = "/user/auth/login"
        user = {"email": user["email"], "password": user["password"]}
        resp = client.post(url, json=user)
        assert resp.status_code == 400
        assert resp.json() == {
            "message": "Your account has not been verified please check your inbox"
        }
