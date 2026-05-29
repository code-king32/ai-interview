from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Job
from app.schemas import JobCreate, JobResponse, JobUpdate

router = APIRouter()

@router.post("/", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    new_job = Job(**job.dict())
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job

@router.get("/", response_model=List[JobResponse])
def get_jobs(db: Session = Depends(get_db)):
    jobs = db.query(Job).all()
    return jobs

@router.get("/{job_id}", response_model=JobResponse)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="职位不存在")
    return job

@router.put("/{job_id}", response_model=JobResponse)
def update_job(job_id: int, job_update: JobUpdate, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="职位不存在")
    
    for key, value in job_update.dict(exclude_unset=True).items():
        setattr(job, key, value)
    
    db.commit()
    db.refresh(job)
    return job

@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="职位不存在")
    db.delete(job)
    db.commit()
    return None