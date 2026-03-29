import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Test data - copy of initial activities for reference
initial_activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Music Ensemble": {
        "description": "Learn instruments and perform in ensembles",
        "schedule": "Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 25,
        "participants": ["ava@mergington.edu", "mason@mergington.edu"]
    },
    "Debate Team": {
        "description": "Competitive debate and public speaking",
        "schedule": "Mondays and Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 14,
        "participants": ["lucas@mergington.edu"]
    },
    "Science Club": {
        "description": "Hands-on experiments and scientific discovery",
        "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": ["isabella@mergington.edu", "ethan@mergington.edu"]
    }
}

def test_root_redirect():
    """Test that root path redirects to static index"""
    # Arrange - No special setup needed
    
    # Act
    response = client.get("/")
    
    # Assert
    assert response.status_code == 307  # Temporary redirect
    assert response.headers["location"] == "/static/index.html"

def test_get_activities():
    """Test getting all activities"""
    # Arrange - No special setup needed
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) == 6  # Should have 6 activities
    
    # Check structure of one activity
    chess_club = data["Chess Club"]
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club
    assert isinstance(chess_club["participants"], list)

def test_signup_success():
    """Test successful signup"""
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    
    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert f"Signed up {email} for {activity_name}" in data["message"]

def test_signup_duplicate():
    """Test signup for already registered student"""
    # Arrange
    activity_name = "Programming Class"
    email = "test@mergington.edu"
    
    # Act - First signup (should succeed)
    client.post(f"/activities/{activity_name}/signup?email={email}")
    
    # Act - Try again (should fail)
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    
    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "already signed up" in data["detail"]

def test_signup_nonexistent_activity():
    """Test signup for non-existent activity"""
    # Arrange
    activity_name = "NonExistent"
    email = "test@mergington.edu"
    
    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]

def test_unregister_success():
    """Test successful unregistration"""
    # Arrange
    activity_name = "Gym Class"
    email = "removeme@mergington.edu"
    
    # Act - First signup
    client.post(f"/activities/{activity_name}/signup?email={email}")
    
    # Act - Then unregister
    response = client.delete(f"/activities/{activity_name}/participants?email={email}")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert f"Unregistered {email} from {activity_name}" in data["message"]

def test_unregister_not_signed_up():
    """Test unregistering student who is not signed up"""
    # Arrange
    activity_name = "Debate Team"
    email = "notsignedup@mergington.edu"
    
    # Act
    response = client.delete(f"/activities/{activity_name}/participants?email={email}")
    
    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "not signed up" in data["detail"]

def test_unregister_nonexistent_activity():
    """Test unregistering from non-existent activity"""
    # Arrange
    activity_name = "NonExistent"
    email = "test@mergington.edu"
    
    # Act
    response = client.delete(f"/activities/{activity_name}/participants?email={email}")
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]