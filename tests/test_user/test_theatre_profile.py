import pytest
from faker import Faker


@pytest.fixture
def theatre_info():
    fake = Faker()
    return {
        "description": "The best movie cinema out there",
        "state": fake.state(),
        "city": fake.city(),
        "street_address": fake.address(),
    }


class TestTheatre:
    def test_theatre_profile_update(self, auth_theatre, client, theatre_info, theatre):
        """
        test theatre profile update
        """
        resp = client.post(
            "/theatre/theatre-address",
            json=theatre_info,
            headers={"Authorization": f"Bearer {auth_theatre}"},
        )
        assert resp.status_code == 201

    def test_unauthenticated_theatre_profile_upload(
        self, client, theatre, theatre_info
    ):
        """
        test un authenticated theatre post profile
        """
        resp = client.post(
            "/theatre/theatre-address",
            json=theatre_info,
            # headers={"Authorization": f"Bearer {auth_theatre}"},
        )
        assert resp.status_code == 403
        assert resp.json() == {"detail": "Not authenticated"}
