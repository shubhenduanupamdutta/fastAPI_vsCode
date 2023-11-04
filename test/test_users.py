import pytest
from app import schemas
from jose import jwt
from app.config.config import secret_key, algorithm


def test_root(client):
    res = client.get("/")
    assert res.json().get('message') == "Welcome to my API"
    assert res.status_code == 200


def test_create_user(client):
    res = client.post("/users/", json={
        "email": "hello@gmail.com",
        "password": "password123"
    })
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "hello@gmail.com"
    assert res.status_code == 201


def test_login_user(client, test_user):
    res = client.post("/login", data={
        "username": test_user["email"],
        "password": test_user["password"]
    })
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, secret_key,
                         algorithms=[algorithm])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@email.com', "pass", 403),
    ('hello@gmail.com', "password", 403),
    ("wrongemail@email.com", "password123", 403),
    (None, "password123", 422),
    ("hello@gmail.com", None, 422)
])
def test_incorrect_login(client, email, password, status_code):
    res = client.post("/login", data={
        "username": email,
        "password": password
    })
    assert res.status_code == status_code
