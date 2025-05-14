from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.schemas import anomalyDetection as schemas

router = APIRouter(prefix="/anomaly-detection", tags=["Anomaly Detection"])

@router.post("/", response_model=schemas.AnomalyDetection)
def create_anomaly(entry: schemas.AnomalyDetectionCreate, db: Session = Depends(get_db)):
    new_entry = models.AnomalyDetection(**entry.dict())
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    
    return new_entry

@router.get("/{entry_id}", response_model=schemas.AnomalyDetection)
def read_anomaly(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(models.AnomalyDetection).filter(models.AnomalyDetection.id == entry_id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Anomaly Detection Entry not found")
    return entry

@router.get("/", response_model = list[schemas.AnomalyDetection])
def read_all_anomalies(db: Session = Depends(get_db)):
    return db.query(models.AnomalyDetection).all()

@router.put("/{entry_id}", response_model = schemas.AnomalyDetection)
def update_anomaly(entry_id: int, updated:schemas.AnomalyDetectionUpdate, db: Session = Depends(get_db)):
    entry = db.query(models.AnomalayDetection).filter(models.AnomalyDetection.id == entry_id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Anomaly Detection Entry not found")
    
    for key, value in updated.dict(exclude_unset=True).items():
        setattr(entry, key, value)
        
    db.commit()
    db.refresh(entry)
    return entry

@router.delete("/{entry_id}")
def delete_anomaly(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(models.AnomalyDetection).filter(models.Anomalyetection.id == entry_id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Anomaly Detection Entry not found")
    
    db.delete(entry)
    db.commit()
    return {"message":"Entry deleted successfully"}
