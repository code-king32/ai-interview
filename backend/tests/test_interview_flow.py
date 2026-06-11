"""面试流程集成测试"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import engine, Base, SessionLocal
from app.models import Job, Candidate, Interview, Message

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup():
    Base.metadata.create_all(bind=engine)
    yield
    db = SessionLocal()
    for m in [Message, Interview, Candidate, Job]:
        db.query(m).delete()
    db.commit()
    db.close()


def test_full_interview_flow():
    """完整面试流程：创建岗位 → 候选人 → 面试 → 对话 → 结束 → 报告"""
    # 1. 创建岗位
    job = client.post("/api/jobs/", json={"title": "流程测试", "description": "D", "requirements": "R"})
    assert job.status_code == 201
    job_id = job.json()["id"]

    # 2. 创建候选人
    cand = client.post("/api/candidates/", json={"name": "测试员"})
    assert cand.status_code == 201
    cand_id = cand.json()["id"]

    # 3. 创建面试
    iv = client.post("/api/interviews/", json={"job_id": job_id, "candidate_id": cand_id})
    assert iv.status_code == 201
    iv_id = iv.json()["id"]
    assert iv.json()["status"] == "pending"

    # 4. 发送对话
    chat = client.post("/api/interviews/chat-v2", json={"interview_id": iv_id, "message": "你好"})
    assert chat.status_code == 200
    assert "assistant_response" in chat.json()

    # 5. 再发一轮
    chat2 = client.post("/api/interviews/chat-v2", json={"interview_id": iv_id, "message": "Spring Boot自动配置通过ImportSelector加载"})
    assert chat2.status_code == 200

    # 6. 结束面试
    end = client.post(f"/api/interviews/{iv_id}/end-v2")
    assert end.status_code == 200
    assert "data" in end.json()

    # 7. 查看报告
    report = client.get(f"/api/reports/{iv_id}")
    assert report.status_code == 200

    # 8. 检查面试状态
    iv_check = client.get(f"/api/interviews/{iv_id}")
    assert iv_check.json()["status"] in ("completed", "COMPLETED")
