from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List

from backend.app.config import get_db
from backend.app.models.sql_models import ResourceSQL, SubjectSQL, UnitSQL
from backend.app.utils.auth_utils import get_current_user_payload

router = APIRouter(prefix="/resources", tags=["Syllabus & Authorized Resources"])

class CreateResourceSchema(BaseModel):
    subject_id: int
    unit_id: Optional[int] = None
    title: str
    resource_type: str # SYLLABUS, NOTES, PYQ, PDF, REFERENCE_LINK
    file_path_or_url: str

@router.post("")
def upload_resource(res_in: CreateResourceSchema, payload: dict = Depends(get_current_user_payload), db: Session = Depends(get_db)):
    if payload.get("role") != "ADMIN":
        raise HTTPException(status_code=403, detail="Only Admins can upload resources")

    res = ResourceSQL(
        subject_id=res_in.subject_id,
        unit_id=res_in.unit_id,
        title=res_in.title,
        resource_type=res_in.resource_type.upper(),
        file_path_or_url=res_in.file_path_or_url
    )
    db.add(res)
    db.commit()
    db.refresh(res)

    return {"message": "Resource uploaded successfully", "resource_id": res.resource_id}

@router.get("/subject/{subject_id}")
def get_resources_by_subject(subject_id: int, resource_type: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(ResourceSQL).filter(ResourceSQL.subject_id == subject_id)
    if resource_type:
        query = query.filter(ResourceSQL.resource_type == resource_type.upper())

    items = query.all()
    results = []
    for r in items:
        results.append({
            "resource_id": r.resource_id,
            "subject_id": r.subject_id,
            "unit_id": r.unit_id,
            "title": r.title,
            "resource_type": r.resource_type,
            "file_path_or_url": r.file_path_or_url,
            "created_at": r.created_at.isoformat() if r.created_at else None
        })
    return results
