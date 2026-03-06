from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_signup_for_activity_success():
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    url = f"/activities/{activity_name}/signup"

    # Act
    response = client.post(url, json={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    activities_response = client.get("/activities")
    assert email in activities_response.json()[activity_name]["participants"]

def test_signup_for_activity_empty_email():
    # Arrange
    activity_name = "Chess Club"
    email = ""
    url = f"/activities/{activity_name}/signup"

    # Act
    response = client.post(url, json={"email": email})

    # Assert
    assert response.status_code == 400 or response.status_code == 422

def test_unregister_from_activity_success():
    # Arrange
    activity_name = "Chess Club"
    email = "removeme@mergington.edu"
    signup_url = f"/activities/{activity_name}/signup"
    unregister_url = f"/activities/{activity_name}/unregister"

    # Act
    # First, sign up the participant
    response1 = client.post(signup_url, json={"email": email})

    # Assert that signup was successful before trying to unregister
    assert response1.status_code == 200
    assert response1.json() == {"message": f"Signed up {email} for {activity_name}"}
    activities_response = client.get("/activities")
    assert email in activities_response.json()[activity_name]["participants"]
    # Then, remove the participant
    response2 = client.post(unregister_url, json={"email": email})

    # Assert that unregister was successful
    assert response2.status_code == 200
    assert response2.json() == {"message": f"Removed {email} from {activity_name}"}
    activities_response = client.get("/activities")
    assert email not in activities_response.json()[activity_name]["participants"]

def test_signup_for_activity_invalid_email():
    # Arrange
    activity_name = "Chess Club"
    email = "testuser1"
    url = f"/activities/{activity_name}/signup"

    # Act
    response = client.post(url, json={"email": email})

    # Assert
    assert response.status_code == 400 or response.status_code == 422
