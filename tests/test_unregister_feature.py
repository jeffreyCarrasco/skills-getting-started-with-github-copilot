import src.app as app_module


def test_unregister_removes_student_from_activity(client):
    email = "michael@mergington.edu"

    response = client.delete("/activities/Chess Club/participants", params={"email": email})

    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from Chess Club"}
    assert email not in app_module.activities["Chess Club"]["participants"]


def test_unregister_returns_not_found_for_unknown_activity(client):
    response = client.delete(
        "/activities/Robotics Club/participants",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_returns_not_found_for_missing_participant(client):
    response = client.delete(
        "/activities/Chess Club/participants",
        params={"email": "absent.student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Participant not found for this activity"}


def test_unregister_allows_student_to_sign_up_again(client):
    email = "michael@mergington.edu"

    unregister_response = client.delete(
        "/activities/Chess Club/participants",
        params={"email": email},
    )
    signup_response = client.post(
        "/activities/Chess Club/signup",
        params={"email": email},
    )

    assert unregister_response.status_code == 200
    assert signup_response.status_code == 200
    assert app_module.activities["Chess Club"]["participants"].count(email) == 1