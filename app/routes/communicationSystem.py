from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.schemas import communicationSystem as schemas

router = APIRouter(prefix="/communication", tags=["Communication System"])

@router.post("/", response_model=schemas.Communication)
def create_communication(entry: schemas.CommunicationCreate, db: Session = Depends(get_db)):
    new_entry = models.CommunicationSystem(**entry.dict())
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry

@router.get("/{entry_id}", response_model=schemas.Communication)
def read_communication(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(models.CommunicationSystem).filter(models.CommunicationSystem.id == entry_id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Communication entry not found")
    return entry

@router.get("/", response_model=list[schemas.Communication])
def read_all_communication(db: Session = Depends(get_db)):
    return db.query(models.CommunicationSystem).all()

@router.put("/{entry_id}", response_model=schemas.Communication)
def update_communication(entry_id: int, updated: schemas.CommunicationUpdate, db: Session = Depends(get_db)):
    entry = db.query(models.CommunicationSystem).filter(models.CommunicationSystem.id == entry_id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Communication entry not found")
    
    for key, value in updated.dict(exclude_unset=True).items():
        setattr(entry, key, value)
    
    db.commit()
    db.refresh(entry)
    return entry

@router.delete("/{entry_iid}")
def delete_communicarion(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(models.CommunicationSystem).filter(models.CommunicationSystem.id == entry_id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Communication entry not found")
    
    db.delete(entry)
    db.commit()
    return{"message": "Entry deleted successfully"}

