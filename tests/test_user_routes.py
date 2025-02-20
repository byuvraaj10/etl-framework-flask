import pytest
from app import create_app, db
from app.database_models import User

@pytest.fixture
def client():
    """Fixture to set up a test client with an in-memory SQLite database."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    client = app.test_client()

    with app.app_context():
        db.create_all()

    yield client  

    with app.app_context():
        db.drop_all()  

def test_create_user(client):
    """Test user creation endpoint."""
    response = client.post('/users', json={"name": "Test User", "email": "test@example.com"})
    assert response.status_code == 201
    assert response.json["message"] == "User created successfully"

def test_get_users(client):
    """Test fetching all users."""
    client.post('/users', json={"name": "Test User", "email": "test@example.com"})
    response = client.get('/users')
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert len(response.json) == 1

def test_get_user(client):
    """Test fetching a single user by ID."""
    client.post('/users', json={"name": "Travis Bickle", "email": "travis@example.com"})
    response = client.get('/users/1')
    assert response.status_code == 200
    assert response.json["name"] == "Travis Bickle"

def test_update_user(client):
    """Test updating an existing user."""
    client.post('/users', json={"name": "Jake Lamotta", "email": "jane@example.com"})
    response = client.put('/users/1', json={"name": "Jake Lamotta", "email": "jake@example.com"})
    assert response.status_code == 200
    assert response.json["message"] == "User updated successfully"

def test_delete_user(client):
    """Test deleting a user."""
    client.post('/users', json={"name": "Mark Twain", "email": "mark@example.com"})
    response = client.delete('/users/1')
    assert response.status_code == 200
    assert response.json["message"] == "User deleted successfully"

def test_create_user_invalid_data(client):
    """Test creating a user with missing data."""
    response = client.post('/users', json={})  
    assert response.status_code == 400
    assert "error" in response.json
