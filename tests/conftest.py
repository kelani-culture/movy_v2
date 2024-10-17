from faker import Faker
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker

from app import app as test_app
from database import Base, get_db
from models.theatre_model import Theatre
from models.user_model import User  # noqa: F401

DATABASE_URL = "sqlite:///:memory:"


engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool
)

TestSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)


@pytest.fixture(scope="function")
def setup_database():
    # Initialize the test database schema
    Base.metadata.create_all(bind=engine)
    yield TestSession
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(setup_database):
    def override_get_db():
        db = TestSession()
        try:
            yield db
        finally:
            db.close()

    test_app.dependency_overrides[get_db] = override_get_db
    client = TestClient(test_app)
    yield client


@pytest.fixture(scope="function")
def db_session(setup_database):
    session = TestSession()
    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture
def theatre():
    faker = Faker()
    return {
        "theatre_name": faker.company(),
        "email": faker.company_email(),
        "password": faker.password(),
    }
# theatre access_token provided
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

# user access token
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