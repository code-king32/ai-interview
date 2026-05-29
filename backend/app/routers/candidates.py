from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Candidate
from app.schemas import CandidateCreate, CandidateResponse, CandidateUpdate
from app.services.resume_parser import ResumeParser
import os

router = APIRouter()

UPLOAD_DIR = "uploads/resumes"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/", response_model=CandidateResponse, status_code=status.HTTP_201_CREATED)
def create_candidate(candidate: CandidateCreate, db: Session = Depends(get_db)):
    db_candidate = db.query(Candidate).filter(Candidate.email == candidate.email).first()
    if db_candidate:
        raise HTTPException(status_code=400, detail="邮箱已被注册")
    
    new_candidate = Candidate(**candidate.dict())
    db.add(new_candidate)
    db.commit()
    db.refresh(new_candidate)
    return new_candidate

@router.post("/upload-resume/{candidate_id}", response_model=CandidateResponse)
def upload_resume(candidate_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="候选人不存在")
    
    allowed_extensions = [".pdf", ".doc", ".docx", ".txt"]
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail="不支持的文件格式，支持：pdf, doc, docx, txt")
    
    file_path = os.path.join(UPLOAD_DIR, f"{candidate_id}_{file.filename}")
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())
    
    resume_parser = ResumeParser()
    resume_text = resume_parser.parse(file_path)
    
    candidate.resume_file_path = file_path
    candidate.resume_text = resume_text
    
    db.commit()
    db.refresh(candidate)
    return candidate

@router.get("/", response_model=List[CandidateResponse])
def get_candidates(db: Session = Depends(get_db)):
    candidates = db.query(Candidate).all()
    return candidates

@router.get("/{candidate_id}", response_model=CandidateResponse)
def get_candidate(candidate_id: int, db: Session = Depends(get_db)):
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="候选人不存在")
    return candidate

@router.put("/{candidate_id}", response_model=CandidateResponse)
def update_candidate(candidate_id: int, candidate_update: CandidateUpdate, db: Session = Depends(get_db)):
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="候选人不存在")
    
    if candidate_update.email:
        db_candidate = db.query(Candidate).filter(Candidate.email == candidate_update.email).first()
        if db_candidate and db_candidate.id != candidate_id:
            raise HTTPException(status_code=400, detail="邮箱已被注册")
    
    for key, value in candidate_update.dict(exclude_unset=True).items():
        setattr(candidate, key, value)
    
    db.commit()
    db.refresh(candidate)
    return candidate

@router.delete("/{candidate_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_candidate(candidate_id: int, db: Session = Depends(get_db)):
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="候选人不存在")
    db.delete(candidate)
    db.commit()
    return None
