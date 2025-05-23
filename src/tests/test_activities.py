from fastapi.testclient import TestClient
from app import app, activities


client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    assert response.json() == activities

def test_signup_for_activity():
    activity_name = "Chess Club"
    email = "test@example.com"
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}

    # Clean up the added participant
    activities[activity_name]["participants"].remove(email)

def test_signup_for_activity_already_signed_up():
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    assert response.status_code == 400
    assert response.json() == {"detail": "Already signed up"}

def test_signup_for_activity_not_found():
    activity_name = "NonExistentActivity"
    email = "test@example.com"
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}
