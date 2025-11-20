from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.dataRecorder import DataRecorder as DataRecorderModel
from app.schemas.dataRecorder import DataRecorderCreate, DataRecorderUpdate, DataRecorder

router = APIRouter(prefix="/data-recorder", tags=["Data Recorder"])

@router.post("/", response_model=DataRecorder)
def create_data_record(entry: DataRecorderCreate, db: Session = Depends(get_db)):
    new_entry = DataRecorderModel(**entry.dict())
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry

@router.get("/{entry_id}", response_model=DataRecorder)
def read_data_record(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(DataRecorderModel).filter(DataRecorderModel.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Data record not found")
    return entry

@router.get("/", response_model=list[DataRecorder])
def read_all_data_records(db: Session = Depends(get_db)):
    return db.query(DataRecorderModel).all()

@router.put("/{entry_id}", response_model=DataRecorder)
def update_data_record(entry_id: int, updated: DataRecorderUpdate, db: Session = Depends(get_db)):
    entry = db.query(DataRecorderModel).filter(DataRecorderModel.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Data record not found")
    
    for key, value in updated.dict(exclude_unset=True).items():
        setattr(entry, key, value)

    db.commit()
    db.refresh(entry)
    return entry

@router.delete("/{entry_id}")
def delete_data_record(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(DataRecorderModel).filter(DataRecorderModel.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Data record not found")
    
    db.delete(entry)
    db.commit()
    return {"detail": "Data record deleted successfully"}
