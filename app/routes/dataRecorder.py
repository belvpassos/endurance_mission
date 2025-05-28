from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.schemas import data_recorder as schemas

router = APIRouter(prefix="/data-recorder", tags=["Data Recorder"])

@router.post("/", response_model=schemas.DataRecorder)
def create_data_record(entry: schemas.DataRecorderCreate, db: Session = Depends(get_db)):
    new_entry = models.DataRecorder(**entry.dict())
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry

@router.get("/{entry_id}", response_model=schemas.DataRecorder)
def read_data_record(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(models.DataRecorder).filter(models.DataRecorder.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Data record not found")
    return entry

@router.get("/", response_model=list[schemas.DataRecorder])
def read_all_data_records(db: Session = Depends(get_db)):
    return db.query(models.DataRecorder).all()

@router.put("/{entry_id}", response_model=schemas.DataRecorder)
def update_data_record(entry_id: int, updated: schemas.DataRecorderUpdate, db: Session = Depends(get_db)):
    entry = db.query(models.DataRecorder).filter(models.DataRecorder.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Data record not found")
    
    for key, value in updated.dict(exclude_unset=True).items():
        setattr(entry, key, value)

    db.commit()
    db.refresh(entry)
    return entry

@router.delete("/{entry_id}")
def delete_data_record(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(models.DataRecorder).filter(models.DataRecorder.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Data record not found")
    
    db.delete(entry)
    db.commit()
    return {"message":"Data record deleted successfully"}
