"""Lab 6: test the PyTodo JSON API directly, with no browser.

Demo login:
    username: demo
    password: demo1234

The API uses the same login as a normal browser session. requests.Session()
keeps the login cookie between calls, the same way a browser keeps it
between page loads. Log in once per test with the logged_in_session
fixture below, already written for you.

Run with:
    pytest test_api.py -v

GET /api/tasks and the first POST test are finished, as your pattern.
Fill in the sections marked TODO.
"""
import os

import pytest
import requests

BASE_URL = os.environ.get("PYTODO_URL", "http://127.0.0.1:5000")


@pytest.fixture
def logged_in_session():
    """Returns a requests.Session already logged in as the demo user."""
    s = requests.Session()
    response = s.post(
        f"{BASE_URL}/login",
        data={"username": "demo", "password": "demo1234"},
    )
    assert response.status_code == 200
    return s


# ============================================================
# GET /api/tasks — finished, your pattern
# ============================================================

def test_get_tasks_requires_login():
    # A plain requests call, no session, no login.
    response = requests.get(f"{BASE_URL}/api/tasks")
    assert response.status_code == 401


def test_get_tasks_returns_json_list(logged_in_session):
    response = logged_in_session.get(f"{BASE_URL}/api/tasks")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert isinstance(response.json(), list)


# ============================================================
# POST /api/tasks — one example finished, one for you to write
# ============================================================

def test_create_task_with_valid_data(logged_in_session):
    payload = {"title": "Write report", "priority": 3, "due_date": "2026-12-01"}
    response = logged_in_session.post(f"{BASE_URL}/api/tasks", json=payload)

    assert response.status_code == 201
    assert response.headers["Content-Type"] == "application/json"

    body = response.json()
    assert body["title"] == "Write report"
    assert body["priority"] == 3
    assert body["due_date"] == "2026-12-01"
    assert body["completed"] is False
    assert "id" in body


def test_create_task_with_invalid_data(logged_in_session):
    payload = {"title": "ab", "priority": 9, "due_date": "2026-12-01"}
    response = logged_in_session.post(f"{BASE_URL}/api/tasks", json=payload)

    assert response.status_code == 400
    body = response.json()
    assert "errors" in body
    assert isinstance(body["errors"], list)
    assert len(body["errors"]) > 0


# ============================================================
# DELETE /api/tasks/<id> — write both of these
# ============================================================

def test_delete_existing_task(logged_in_session):
    created = logged_in_session.post(
        f"{BASE_URL}/api/tasks",
        json={"title": "Temp task", "priority": 2, "due_date": "2026-12-01"},
    )
    task_id = created.json()["id"]

    response = logged_in_session.delete(f"{BASE_URL}/api/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json() == {"status": "deleted", "id": task_id}


def test_delete_missing_task_returns_404(logged_in_session):
    response = logged_in_session.delete(f"{BASE_URL}/api/tasks/999999")
    assert response.status_code == 404                         


# ============================================================
# Full flow — create, read it back, delete, confirm it is gone
# ============================================================

def test_create_read_delete_flow(logged_in_session):
    # create
    created = logged_in_session.post(
        f"{BASE_URL}/api/tasks",
        json={"title": "Flow task", "priority": 1, "due_date": "2026-12-01"},
    )
    assert created.status_code == 201
    task_id = created.json()["id"]

    # read: it should be in the list
    tasks = logged_in_session.get(f"{BASE_URL}/api/tasks").json()
    assert any(t["id"] == task_id for t in tasks)

    # delete
    deleted = logged_in_session.delete(f"{BASE_URL}/api/tasks/{task_id}")
    assert deleted.status_code == 200

    # read again: it should be gone
    tasks = logged_in_session.get(f"{BASE_URL}/api/tasks").json()
    assert not any(t["id"] == task_id for t in tasks)
