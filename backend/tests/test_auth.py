"""
认证 API 测试
运行: cd backend && python -m pytest tests/ -v
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import engine, Base
from app.models import User

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    # 清理测试用户
    from app.database import SessionLocal
    db = SessionLocal()
    db.query(User).filter(User.username.like("test_%")).delete()
    db.commit()
    db.close()


def test_health():
    resp = client.get("/api/health")
    assert resp.status_code == 200
    assert resp.json()["code"] == 0


def test_register():
    resp = client.post("/api/auth/register", json={
        "username": "test_user_1", "password": "123456", "role": "seeker"
    })
    assert resp.status_code == 200
    assert resp.json()["message"] == "注册成功"


def test_register_duplicate():
    client.post("/api/auth/register", json={
        "username": "test_user_2", "password": "123456", "role": "hr"
    })
    resp = client.post("/api/auth/register", json={
        "username": "test_user_2", "password": "123456", "role": "hr"
    })
    assert resp.status_code == 400


def test_register_weak_password():
    resp = client.post("/api/auth/register", json={
        "username": "test_user_3", "password": "12", "role": "seeker"
    })
    assert resp.status_code == 400


def test_login():
    client.post("/api/auth/register", json={
        "username": "test_user_4", "password": "123456", "role": "hr"
    })
    resp = client.post("/api/auth/login", json={
        "username": "test_user_4", "password": "123456"
    })
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data["role"] == "hr"


def test_login_wrong_password():
    resp = client.post("/api/auth/login", json={
        "username": "test_user_4", "password": "wrong"
    })
    assert resp.status_code == 401
