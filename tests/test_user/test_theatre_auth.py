import os

import pytest
from faker import Faker
from PIL import Image

from models.theatre_model import Theatre


@pytest.fixture
def theatre():
    faker = Faker()
    return {
        "theatre_name": faker.company(),
        "email": faker.company_email(),
        "password": faker.password(),
    }


@pytest.fixture
def auth_theatre(db_session, client, theatre):
    user_d = Theatre(**theatre)
    user_d.is_verified = True  # Set user as verified
    db_session.add(user_d)
    db_session.commit()  # Commit the user to the session

    # Check if the user was saved correctly
    db_session.refresh(user_d)  # Refresh to get updated state from the database

    url = "/theatre/auth/login"
    user_login_data = {"email": theatre["email"], "password": theatre["password"]}
    resp = client.post(url, json=user_login_data)
    return resp.json()["access_token"]


class TestTheatreAuth:
    def setup_method(self, method):
        self.image_path = "theater_test_image.jpg"
        image = Image.new(
            "RGB", (200, 200), color="green"
        )  # create fake image for test
        image.save(self.image_path)

        # create fake file for invalid image
        self.fake_file = "theatre_file.pdf"
        with open(self.fake_file, "w") as f:
            f.write("fake theatre file")

    def teardown_method(self, method):
        if os.path.exists(self.image_path):
            os.remove(self.image_path)

        if os.path.exists(self.fake_file):
            os.remove(self.fake_file)

    def test_theatre_signup(self, client, theatre):
        """
        test theatre signup
        """
        url = "/theatre/auth/signup"
        resp = client.post(url, json=theatre)
        assert resp.status_code == 201
        assert resp.json() == {
            "message": "Theatre created successfully",
            "status_code": 201,
        }

    def test_create_theatre_unsuccessful(self, client, db_session, theatre):
        """
        test create theatre unsuccessful
        """
        user_d = Theatre(**theatre)
        db_session.add(user_d)
        db_session.commit()

        url = "/theatre/auth/signup"
        resp = client.post(url, json=theatre)
        print(resp.json())
        resp_msg = {"message": "User email already exists please proceed to login"}
        assert resp.status_code == 400
        assert resp.json() == resp_msg

    def test_theatre_login(self, client, theatre, db_session):
        """
        test theatre login
        """
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

    def test_theatrer_email_not_verified(self, client, theatre, db_session):
        """
        test theatre email not verified
        """
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

    def test_theatre_invalid_email(self, client, theatre):
        """
        test theatre invalid email
        """
        url = "/theatre/auth/login"
        user = {"email": theatre["email"], "password": theatre["password"]}
        resp = client.post(url, json=user)
        assert resp.status_code == 400
        assert resp.json() == {"message": "Invalid email or password provided"}

    def test_theatre_account_disabled(self, client, theatre, db_session):
        """
        test theatre account disabled
        """
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

    def test_theatre_account_not_verified(self, client, theatre, db_session):
        """
        test theatre account verified
        """
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

    def test_theatre_upload_image(self, client, auth_theatre, db_session, theatre):
        """
        test theatre upload image
        """
        # user_d = Theatre(**theatre)
        # user_d.is_verified = True  # Set user as verified
        # db_session.add(user_d)
        # db_session.commit()  # Commit the user to the session

        with open(self.image_path, "rb") as f:
            response = client.patch(
                "/theatre/upload-profile-image",
                files={"pic": (self.image_path, f, "image/jpeg")},
                headers={"Authorization": f"Bearer {auth_theatre}"},
            )
        print(response.json())
        assert response.status_code == 200
        assert os.path.exists(response.json()["profile_path"])

        os.remove(response.json()["profile_path"])

    def test_theatre_upload_invalid_image(self, client, auth_theatre):
        """
        test invalid file upload
        """
        with open(self.fake_file, "rb") as f:
            response = client.patch(
                "/theatre/upload-profile-image",
                files={"pic": (self.fake_file, f, "image/jpeg")},
                headers={"Authorization": f"Bearer {auth_theatre}"},
            )
        assert response.status_code == 400
        assert response.json() == {"message": "Invalid image file"}

    def test_unauthenticate_user_upload_file(self, client, db_session, theatre):
        """
        test unauthenticated theatre upload
        """
        user_d = Theatre(**theatre)
        user_d.is_verified = True
        db_session.add(user_d)
        db_session.commit()

        with open(self.image_path, "rb") as f:
            response = client.patch(
                "/user/upload-profile-image",
                files={"pic": (self.image_path, f, "image/jpeg")},
                # headers={"Authorization": f"Bearer {auth_user}"},
            )
        assert response.status_code == 403
        print(response.json())
        assert response.json() == {"detail": "Not authenticated"}
