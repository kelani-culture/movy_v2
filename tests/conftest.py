import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker

from app import app as test_app
from database import Base, get_db
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
