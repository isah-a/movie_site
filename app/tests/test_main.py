import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Creating a new engine and session for testing
# We are using an in-memory database for tests
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

# Dependency override to use the test database
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

#Testing User Registration
def test_user_registration():
    response = client.post("/users/", json={"username": "testuser", "password": "testpass", "email": "test@example.com", "country": "Testland"})
    assert response.status_code == 201
    assert response.json()["username"] == "testuser"

# Testing User Login
def test_user_login():
    response = client.post("/login", data={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200
    assert "access_token" in response.json()

#Testing Movie Creation
def test_create_movie():
    # Log in to get token
    login_response = client.post("/login", data={"username": "testuser", "password": "testpass"})
    token = login_response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/movies/", json={"title": "Test Movie", "description": "A test movie."}, headers=headers)
    assert response.status_code == 201
    assert response.json()["title"] == "Test Movie"

#Testing View All Movies
def test_view_all_movies():
    response = client.get("/movies/")
    assert response.status_code == 200
    assert len(response.json()) > 0

#Testing Update Movie
def test_update_movie():
    # Log in to get token
    login_response = client.post("/login", data={"username": "testuser", "password": "testpass"})
    token = login_response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    response = client.put("/movies/1", json={"title": "Updated Movie", "description": "Updated description."}, headers=headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Movie"

#Testing Delete Movie
def test_delete_movie():
    # Log in to get token
    login_response = client.post("/login", data={"username": "testuser", "password": "testpass"})
    token = login_response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    response = client.delete("/movies/1", headers=headers)
    assert response.status_code == 204

#Testing Add Rating
def test_add_rating():
    # Log in to get token
    login_response = client.post("/login", data={"username": "testuser", "password": "testpass"})
    token = login_response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/ratings/", json={"score": 5, "movie_id": 1}, headers=headers)
    assert response.status_code == 201
    assert response.json()["score"] == 5

#Testing Add Comment
def test_add_comment():
    # Log in to get token
    login_response = client.post("/login", data={"username": "testuser", "password": "testpass"})
    token = login_response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/comments/", json={"content": "Great movie!", "movie_id": 1}, headers=headers)
    assert response.status_code == 201
    assert response.json()["content"] == "Great movie!"

#Testing View Comments for a Movie
def test_view_comments():
    response = client.get("/comments/?movie_id=1")
    assert response.status_code == 200
    assert len(response.json()) > 0
