from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.schemas import payloadSystem as schemas

router = APIRouter(prefix="/payload-system", tags=["Payload System"])


@router.post("/", response_model=schemas.PayloadSystem)
def create_payload(entry: schemas.PayloadSystemCreate, db: Session = Depends(get_db)):
    new_entry = models.PayloadSystem(**entry.dict())
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry

@router.get("/{entry_id}", response_model=schemas.PayloadSystem)
def read_payload(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(models.PayloadSystem).filter(models.PayloadSystem.id == entry_id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Payload entry not found")
    return entry

@router.get("/", response_model=list[schemas.PayloadSystem])
def read_all_payload(db: Session = Depends(get_db)):
    return db.query(models.PayloadSystem).all()

@router.put("/{entry_id}", response_model=schemas.payloadSystem)
def update_payload(entry_id: int, updated: schemas.PayloadSystemUpdate, db: Session = Depends(get_db)):
    entry = db.query(models.PayloadSystem).filter(models.PayloadSystem.id == entry_id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail= "Payload entry not found")
    for key, value in updated.dict(exclude_unset=True).item():
        setattr(entry, key, value)
        
    db.commit()
    db.refresh(entry)
    return entry
        

@router.delete("/{entry_id}")
def delete_payload(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(models.PayloadSystem).filter(models.PayloadSystem.id == entry_id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Payload entry not found")
    
    db.delete(entry)
    db.commit()
    return {"message":"Payload entry deleted successfully"}