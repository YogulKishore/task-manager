import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from backend.database import Base, get_db

SQLALCHEMY_TEST_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_TEST_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
Base.metadata.create_all(bind=engine)

client = TestClient(app)


def register_and_login(username="testuser", password="testpass123"):
    client.post("/register", json={
        "username": username,
        "email": f"{username}@test.com",
        "password": password,
    })
    res = client.post("/login", json={"username": username, "password": password})
    return res.json()["access_token"]


def auth(token):
    return {"Authorization": f"Bearer {token}"}


def test_register_success():
    res = client.post("/register", json={
        "username": "newuser",
        "email": "newuser@test.com",
        "password": "password123",
    })
    assert res.status_code == 201
    assert res.json()["username"] == "newuser"


def test_register_duplicate_username():
    client.post("/register", json={"username": "dupeuser", "email": "a@a.com", "password": "pass"})
    res = client.post("/register", json={"username": "dupeuser", "email": "b@b.com", "password": "pass"})
    assert res.status_code == 400
    assert "username" in res.json()["detail"].lower()


def test_login_success():
    token = register_and_login("logintest")
    assert token is not None


def test_login_wrong_password():
    register_and_login("wrongpass")
    res = client.post("/login", json={"username": "wrongpass", "password": "badpassword"})
    assert res.status_code == 401


def test_create_task():
    token = register_and_login("taskuser1")
    res = client.post("/tasks", json={"title": "Buy groceries"}, headers=auth(token))
    assert res.status_code == 201
    assert res.json()["title"] == "Buy groceries"
    assert res.json()["completed"] is False


def test_get_tasks():
    token = register_and_login("taskuser2")
    client.post("/tasks", json={"title": "Task A"}, headers=auth(token))
    client.post("/tasks", json={"title": "Task B"}, headers=auth(token))
    res = client.get("/tasks", headers=auth(token))
    assert res.status_code == 200
    assert res.json()["total"] >= 2


def test_get_single_task():
    token = register_and_login("taskuser3")
    created = client.post("/tasks", json={"title": "Single task"}, headers=auth(token)).json()
    res = client.get(f"/tasks/{created['id']}", headers=auth(token))
    assert res.status_code == 200
    assert res.json()["title"] == "Single task"


def test_mark_task_completed():
    token = register_and_login("taskuser4")
    task = client.post("/tasks", json={"title": "Complete me"}, headers=auth(token)).json()
    res = client.put(f"/tasks/{task['id']}", json={"completed": True}, headers=auth(token))
    assert res.status_code == 200
    assert res.json()["completed"] is True


def test_delete_task():
    token = register_and_login("taskuser5")
    task = client.post("/tasks", json={"title": "Delete me"}, headers=auth(token)).json()
    res = client.delete(f"/tasks/{task['id']}", headers=auth(token))
    assert res.status_code == 204
    res2 = client.get(f"/tasks/{task['id']}", headers=auth(token))
    assert res2.status_code == 404


def test_task_isolation():
    token_a = register_and_login("isolation_a")
    token_b = register_and_login("isolation_b")
    task = client.post("/tasks", json={"title": "Private task"}, headers=auth(token_a)).json()
    res = client.get(f"/tasks/{task['id']}", headers=auth(token_b))
    assert res.status_code == 404


def test_filter_completed():
    token = register_and_login("filteruser")
    t = client.post("/tasks", json={"title": "Filter test"}, headers=auth(token)).json()
    client.put(f"/tasks/{t['id']}", json={"completed": True}, headers=auth(token))
    res = client.get("/tasks?completed=true", headers=auth(token))
    assert all(task["completed"] for task in res.json()["tasks"])


def test_unauthenticated_access():
    res = client.get("/tasks")
    assert res.status_code == 401
