from ctypes.wintypes import RGB
import os
from pathlib import Path
import pytest
from PIL import Image
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

def create_image(image_file: str):
    image = Image.new("RGB", (100, 100), color="blue")
    image.save(image_file)

@pytest.fixture
def test_image_file():
    # Create a dummy test image file

    file_path = "test_image.jpg"
    create_image(file_path)
    # file_path = Path("test_image.jpg")
    # with open(file_path, "wb") as f:
    #     f.write(os.urandom(1024))# Dummy content for testing
    # yield file_path
    # file_path.unlink()  # Clean up the file after the test
    # return file_path

