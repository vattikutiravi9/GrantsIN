import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app
from models import User, Grant

# Set up a test database using SQLite in-memory
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Override the get_db dependency to use the test database
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    # Create the database and tables
    Base.metadata.create_all(bind=engine)
    yield
    # Drop the tables after the test runs
    Base.metadata.drop_all(bind=engine)


def test_apply_for_grant_success():
    # Add a test user and grant
    db = TestingSessionLocal()
    test_user = User(
        username="testuser", email="testuser@example.com", hashed_password="fakehash"
    )
    test_grant = Grant(
        title="Test Grant",
        description="A test grant",
        category="Education",
        created_by=1,
    )
    db.add(test_user)
    db.add(test_grant)
    db.commit()

    # Create a mock token
    token = "Bearer valid_test_token"

    # Prepare the file upload data
    files = {"files": ("test.pdf", b"fake content", "application/pdf")}

    response = client.post(
        f"/grants/{test_grant.id}/apply", headers={"Authorization": token}, files=files
    )

    assert response.status_code == 200
    assert response.json() == {"message": "Application submitted successfully"}


def test_apply_for_grant_invalid_grant():
    # Create a mock token
    token = "Bearer valid_test_token"

    # Prepare the file upload data
    files = {"files": ("test.pdf", b"fake content", "application/pdf")}

    response = client.post(
        "/grants/999/apply",  # Non-existing grant ID
        headers={"Authorization": token},
        files=files,
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Grant not found"}


def test_apply_for_grant_invalid_file_type():
    # Add a test user and grant
    db = TestingSessionLocal()
    test_user = User(
        username="testuser", email="testuser@example.com", hashed_password="fakehash"
    )
    test_grant = Grant(
        title="Test Grant",
        description="A test grant",
        category="Education",
        created_by=1,
    )
    db.add(test_user)
    db.add(test_grant)
    db.commit()

    # Create a mock token
    token = "Bearer valid_test_token"

    # Prepare the file upload data with an invalid file type
    files = {"files": ("test.txt", b"fake content", "text/plain")}

    response = client.post(
        f"/grants/{test_grant.id}/apply", headers={"Authorization": token}, files=files
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid file type"}


def test_grant_without_token():

    # Prepare the file upload data with an invalid file type
    files = {"files": ("test.txt", b"fake content", "text/plain")}

    response = client.post(f"/grants/{1}/apply", files=files)

    assert response.status_code == 403
    assert response.json() == {"detail": "Not authenticated"}
