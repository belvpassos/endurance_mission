# app/routes/softwareUpdateLog.py

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import softwareUpdateLog as models
from app.schemas import softwareUpdateLog as schemas
from app.schemas.common import OperationStatus

router = APIRouter(prefix="/software-update-log", tags=["Software Update Log"])

@router.post("/", response_model=schemas.SoftwareUpdateLog, status_code=status.HTTP_201_CREATED)
def create_update_log(entry: schemas.SoftwareUpdateLogCreate, db: Session = Depends(get_db)):
    new_entry = models.SoftwareUpdateLog(**entry.model_dump())
    db.add(new_entry)
    try:
        db.commit()
        db.refresh(new_entry)
        return new_entry
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not create software update log entry: {exc}")

@router.get("/{entry_id}", response_model=schemas.SoftwareUpdateLog)
def read_update_log(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(models.SoftwareUpdateLog).filter(models.SoftwareUpdateLog.id == entry_id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Log not found")
    return entry

@router.get("/", response_model=list[schemas.SoftwareUpdateLog])
def read_all_update_logs(db: Session = Depends(get_db)):
    return db.query(models.SoftwareUpdateLog).all()

@router.put("/{entry_id}", response_model=schemas.SoftwareUpdateLog)
def update_update_log(entry_id: int, updated: schemas.SoftwareUpdateLogUpdate, db: Session = Depends(get_db)):
    entry = db.query(models.SoftwareUpdateLog).filter(models.SoftwareUpdateLog.id == entry_id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Log not found")

    for key, value in updated.model_dump(exclude_unset=True).items():
        setattr(entry, key, value)

    try:
        db.commit()
        db.refresh(entry)
        return entry
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not update software update log entry: {exc}")

@router.delete("/{entry_id}", response_model=OperationStatus)
def delete_update_log(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(models.SoftwareUpdateLog).filter(models.SoftwareUpdateLog.id == entry_id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Log not found")
    
    db.delete(entry)
    try:
        db.commit()
        return OperationStatus(detail="Software update log entry deleted successfully")
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not delete software update log entry: {exc}")
