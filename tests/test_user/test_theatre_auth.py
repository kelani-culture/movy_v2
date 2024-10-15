import pytest
from faker import Faker

from models.theatre_model import Theatre


@pytest.fixture
def theatre():
    faker = Faker()
    return {
        "theatre_name": faker.company(),
        "email": faker.company_email(),
        "password": faker.password(),
    }


class TestTheatreAuth:
    def test_theatre_signup(self, client, theatre):
        url = "/theatre/auth/signup"
        print(theatre)
        resp = client.post(url, json=theatre)
        assert resp.status_code == 201
        assert resp.json() == {
            "message": "Theatre created successfully",
            "status_code": 201,
        }

    def test_create_user_unsuccessful(self, client, db_session, theatre):
        user_d = Theatre(**theatre)
        db_session.add(user_d)
        db_session.commit()

        url = "/theatre/auth/signup"
        resp = client.post(url, json=theatre)
        resp_msg = {"message": "User email already exists please proceed to login"}
        assert resp.status_code == 400
        assert resp.json() == resp_msg

    def test_user_login(self, client, theatre, db_session):
        user_d = Theatre(**theatre)
        user_d.is_verified = True
        db_session.add(user_d)
        db_session.commit()

        url = "/theatre/auth/login"
        user = {"email": theatre["email"], "password": theatre["password"]}
        resp = client.post(url, json=user)
        print(resp.json())
        assert resp.status_code == 200
        assert "access_token" in resp.json()
        assert "refresh_token" in resp.json()
        assert "theatre_name" in resp.json()
        assert "profile_pic" in resp.json()
        assert "expires_at" in resp.json()

    def test_user_email_not_verified(self, client, theatre, db_session):
        user_d = Theatre(**theatre)
        db_session.add(user_d)
        db_session.commit()

        url = "/theatre/auth/login"
        user = {"email": theatre["email"], "password": theatre["password"]}
        resp = client.post(url, json=user)
        assert resp.status_code == 400
        assert resp.json() == {
            "message": "Your account has not been verified please check your inbox"
        }

    def test_user_invalid_email(self, client, theatre):
        url = "/theatre/auth/login"
        user = {"email": theatre["email"], "password": theatre["password"]}
        resp = client.post(url, json=user)
        assert resp.status_code == 400
        assert resp.json() == {"message": "Invalid email or password provided"}

    def test_user_account_disabled(self, client, theatre, db_session):
        user_d = Theatre(**theatre)
        user_d.is_active = False
        db_session.add(user_d)
        db_session.commit()

        url = "/theatre/auth/login"
        user = {"email": theatre["email"], "password": theatre["password"]}
        resp = client.post(url, json=user)
        assert resp.status_code == 400
        assert resp.json() == {
            "message": "Your account has been disabled please contact admin"
        }

    def test_user_account_not_verified(self, client, theatre, db_session):
        user_d = Theatre(**theatre)
        user_d.is_verified = False
        db_session.add(user_d)
        db_session.commit()

        url = "/theatre/auth/login"
        user = {"email": theatre["email"], "password": theatre["password"]}
        resp = client.post(url, json=user)
        assert resp.status_code == 400
        assert resp.json() == {
            "message": "Your account has not been verified please check your inbox"
        }
