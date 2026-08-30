def test_root_redirects_to_static_index(client):
    response = client.get("/", follow_redirects=False)
    assert response.status_code in (307, 308)
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_known_activities(client):
    response = client.get("/activities")
    assert response.status_code == 200

    data = response.json()
    assert "Chess Club" in data

    chess_club = data["Chess Club"]
    assert set(["description", "schedule", "max_participants", "participants"]) <= set(chess_club.keys())


def test_signup_for_activity_success(client):
    email = "newstudent@mergington.edu"
    response = client.post(f"/activities/Chess Club/signup?email={email}")
    assert response.status_code == 200

    activities = client.get("/activities").json()
    assert email in activities["Chess Club"]["participants"]


def test_signup_for_unknown_activity_returns_404(client):
    response = client.post("/activities/Not A Club/signup?email=someone@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_duplicate_returns_400(client):
    email = "michael@mergington.edu"  # already signed up for Chess Club
    response = client.post(f"/activities/Chess Club/signup?email={email}")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_from_activity_success(client):
    email = "michael@mergington.edu"  # already signed up for Chess Club
    response = client.delete(f"/activities/Chess Club/participants?email={email}")
    assert response.status_code == 200

    activities = client.get("/activities").json()
    assert email not in activities["Chess Club"]["participants"]


def test_unregister_from_unknown_activity_returns_404(client):
    response = client.delete("/activities/Not A Club/participants?email=someone@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_student_not_signed_up_returns_404(client):
    response = client.delete("/activities/Chess Club/participants?email=notsignedup@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"
