from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import anomalyDetection as models
from app.schemas import anomalyDetection as schemas
from app.schemas.common import OperationStatus

router = APIRouter(prefix="/anomaly-detection", tags=["Anomaly Detection"])

@router.post("/", response_model=schemas.AnomalyDetection, status_code=status.HTTP_201_CREATED)
def create_anomaly(entry: schemas.AnomalyDetectionCreate, db: Session = Depends(get_db)):
    try:
        new_entry = models.AnomalyDetection(**entry.model_dump())
        db.add(new_entry)
        db.commit()
        db.refresh(new_entry)
        return new_entry
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not create anomaly detection entry: {exc}")

@router.get("/{entry_id}", response_model=schemas.AnomalyDetection)
def read_anomaly(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(models.AnomalyDetection).filter(models.AnomalyDetection.id == entry_id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Anomaly Detection entry not found")
    return entry

@router.get("/", response_model=list[schemas.AnomalyDetection])
def read_all_anomalies(db: Session = Depends(get_db)):
    return db.query(models.AnomalyDetection).all()

@router.put("/{entry_id}", response_model=schemas.AnomalyDetection)
def update_anomaly(entry_id: int, updated: schemas.AnomalyDetectionUpdate, db: Session = Depends(get_db)):
    entry = db.query(models.AnomalyDetection).filter(models.AnomalyDetection.id == entry_id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Anomaly Detection entry not found")

    try:
        for key, value in updated.model_dump(exclude_unset=True).items():
            setattr(entry, key, value)
        db.commit()
        db.refresh(entry)
        return entry
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not update anomaly detection entry: {exc}")

@router.delete("/{entry_id}", response_model=OperationStatus)
def delete_anomaly(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(models.AnomalyDetection).filter(models.AnomalyDetection.id == entry_id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Anomaly Detection entry not found")

    try:
        db.delete(entry)
        db.commit()
        return OperationStatus(detail="Anomaly detection entry deleted successfully")
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not delete anomaly detection entry: {exc}")
