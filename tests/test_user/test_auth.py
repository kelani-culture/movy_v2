import pytest
from faker import Faker


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
    def test_create_user(self, client, db_session, user):
        url = "/user/auth/signup"
        resp = client.post(url, json=user)
        assert resp.status_code == 201
        assert resp.json() == {"message": "User created successfully", "status_code": 201}

    def test_user_login(self, client, user):
        ...