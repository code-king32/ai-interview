import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.invite import InviteToken
from app.models.job import Job
from app.models.candidate import Candidate
from app.models.interview import Interview
from app.models.interview import InterviewStatus

router = APIRouter()


@router.post("/jobs/{job_id}/invite")
def create_invite(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="岗位不存在")

    token = InviteToken(token=uuid.uuid4().hex, job_id=job_id)
    db.add(token)
    db.commit()
    db.refresh(token)

    return {
        "code": 0,
        "message": "邀请链接已生成",
        "data": {
            "token": token.token,
            "url": f"/invite/{token.token}",
        },
    }


@router.get("/jobs/{job_id}/invites")
def list_invites(job_id: int, db: Session = Depends(get_db)):
    tokens = db.query(InviteToken).filter(InviteToken.job_id == job_id).order_by(InviteToken.created_at.desc()).all()
    return {
        "code": 0,
        "data": [
            {
                "id": t.id,
                "token": t.token,
                "url": f"/invite/{t.token}",
                "used": t.used,
                "candidate_id": t.candidate_id,
                "created_at": t.created_at.isoformat() if t.created_at else None,
            }
            for t in tokens
        ],
    }


@router.get("/invite/{token}")
def get_invite(token: str, db: Session = Depends(get_db)):
    t = db.query(InviteToken).filter(InviteToken.token == token).first()
    if not t:
        raise HTTPException(status_code=404, detail="邀请链接无效或已过期")

    job = db.query(Job).filter(Job.id == t.job_id).first()
    return {
        "code": 0,
        "data": {
            "token": t.token,
            "used": t.used,
            "job": {"id": job.id, "title": job.title, "description": job.description} if job else None,
        },
    }


@router.post("/invite/{token}/start")
async def start_invite_interview(
    token: str,
    name: str = Form(...),
    email: str = Form(""),
    phone: str = Form(""),
    resume: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    t = db.query(InviteToken).filter(InviteToken.token == token).first()
    if not t:
        raise HTTPException(status_code=404, detail="邀请链接无效或已过期")
    if t.used:
        raise HTTPException(status_code=400, detail="该邀请已被使用")

    # 创建候选人
    candidate = Candidate(name=name, email=email, phone=phone)
    db.add(candidate)
    db.flush()

    # 上传简历
    if resume and resume.filename:
        import os
        upload_dir = "uploads/resumes"
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, f"{candidate.id}_{resume.filename}")
        with open(file_path, "wb") as f:
            f.write(await resume.read())
        candidate.resume_file_path = file_path

        # 解析简历
        ext = os.path.splitext(resume.filename)[1].lower()
        if ext == ".txt":
            with open(file_path, "r", encoding="utf-8") as f:
                candidate.resume_text = f.read()
        elif ext == ".pdf":
            try:
                from PyPDF2 import PdfReader
                reader = PdfReader(file_path)
                candidate.resume_text = "\n".join(p.extract_text() or "" for p in reader.pages)
            except Exception:
                pass
        elif ext in (".docx", ".doc"):
            try:
                from docx import Document
                candidate.resume_text = "\n".join(p.text for p in Document(file_path).paragraphs)
            except Exception:
                pass

    db.commit()
    db.refresh(candidate)

    # 创建面试
    interview = Interview(
        job_id=t.job_id,
        candidate_id=candidate.id,
        status=InterviewStatus.PENDING,
    )
    db.add(interview)
    db.flush()

    # 标记邀请已使用
    t.used = True
    t.candidate_id = candidate.id
    db.commit()
    db.refresh(interview)

    return {
        "code": 0,
        "message": "面试已创建",
        "data": {
            "interview_id": interview.id,
            "candidate_name": candidate.name,
        },
    }
