"""Part 2: tests against JSONPlaceholder, a public API.

Complete API_FINDINGS.md before writing any test in this file. Each
assertion below should state what you recorded there, not a value
copied from the documentation.

Run with:
    pytest test_public_api.py -v
"""
import requests

BASE_URL = "https://jsonplaceholder.typicode.com"


def test_get_single_post():
    response = requests.get(f"{BASE_URL}/posts/1")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json; charset=utf-8"

    body = response.json()
    assert isinstance(body["userId"], int)
    assert isinstance(body["id"], int)
    assert isinstance(body["title"], str)
    assert isinstance(body["body"], str)
    assert body["id"] == 1


def test_get_all_posts():
    response = requests.get(f"{BASE_URL}/posts")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json; charset=utf-8"

    body = response.json()
    assert isinstance(body, list)
    assert len(body) == 100
    first = body[0]
    assert set(first.keys()) == {"userId", "id", "title", "body"}


def test_create_post():
    payload = {"title": "foo", "body": "bar", "userId": 1}
    response = requests.post(f"{BASE_URL}/posts", json=payload)
    assert response.status_code == 201
    assert response.headers["Content-Type"] == "application/json; charset=utf-8"

    body = response.json()
    assert body["title"] == "foo"
    assert body["body"] == "bar"
    assert body["userId"] == 1
    assert isinstance(body["id"], int)   # the field the server adds


def test_delete_post():
    response = requests.delete(f"{BASE_URL}/posts/1")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json; charset=utf-8"
    assert response.json() == {}
