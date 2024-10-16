import os

import pytest
from faker import Faker
from PIL import Image

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


@pytest.fixture
def auth_user(db_session, client, user):
    user_d = User(**user)
    user_d.is_verified = True  # Set user as verified
    db_session.add(user_d)
    db_session.commit()  # Commit the user to the session

    # Check if the user was saved correctly
    db_session.refresh(user_d)  # Refresh to get updated state from the database

    url = "/user/auth/login"
    user_login_data = {"email": user["email"], "password": user["password"]}
    resp = client.post(url, json=user_login_data)
    return resp.json()["access_token"]


class TestUserAuth:
    # @pytest.fixture(autouse=True)
    def setup_method(self, method):
        """
        set up file
        """
        print("setting up environment......")
        self.image_path = "test_image.jpg"
        image = Image.new("RGB", (100, 100), color="blue")
        image.save(self.image_path)

        self.file = "invalid_file.pdf"

        with open(self.file, "w") as f:  # create none image file
            f.write("faker file i guess")

    # @pytest.fixture(autouse=True)
    def teardown_method(self, method):
        """
        tear down file
        """
        print("tearing down image..................")
        if os.path.exists(self.image_path) or os.path.exists(self.file):
            os.remove(self.image_path)
            os.remove(self.file)

    def test_image_creation(self):
        assert os.path.exists(self.image_path) is True

    def test_create_user_successful(self, client, user):
        """
        test user successful login
        """
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
        """
        test user successful login
        """
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
        """
        test user email not verified
        """
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
        """
        test user valide email
        """
        url = "/user/auth/login"
        user = {"email": user["email"], "password": user["password"]}
        resp = client.post(url, json=user)
        assert resp.status_code == 400
        assert resp.json() == {"message": "Invalid email or password provided"}

    def test_user_account_disabled(self, client, user, db_session):
        """
        test user account disabled
        """
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
        """
        test user account not verified
        """
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

    def test_user_image_upload(self, client, auth_user):
        """
        test authenticated user can upload profile image using
        """
        with open(self.image_path, "rb") as f:
            response = client.patch(
                "/user/upload-profile-image",
                files={"pic": (self.image_path, f, "image/jpeg")},
                headers={"Authorization": f"Bearer {auth_user}"},
            )
        assert response.status_code == 200
        assert os.path.exists(response.json()["profile_path"])

        os.remove(response.json()["profile_path"])

    def test_user_upload_invalid_image(self, client, auth_user):
        """
        test invalid file upload
        """
        with open(self.file, "rb") as f:
            response = client.patch(
                "/user/upload-profile-image",
                files={"pic": (self.file, f, "image/jpeg")},
                headers={"Authorization": f"Bearer {auth_user}"},
            )
        assert response.status_code == 400
        assert response.json() == {"message": "Invalid image file"}

    def test_unauthenticate_user_upload_file(self, client, db_session, user):
        """
        test unauthenticated user upload
        """
        user_d = User(**user)
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
