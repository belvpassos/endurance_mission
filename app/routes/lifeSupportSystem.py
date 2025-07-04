from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.schemas import lifeSupportSystem as schemas

router = APIRouter(prefix="/life-support", tags=["Life Support System"])


@router.post("/", response_model=schemas.LifeSupportSystem)
def create_entry(entry: schemas.LifeSupportSystemCreate, db: Session = Depends(get_db)):
    new_entry = models.LifeSupportSystem(**entry.dict())
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry


@router.get("/{entry_id}", response_model=schemas.LifeSupportSystem)
def read_entry(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(models.LifeSupportSystem).filter(models.LifeSupportSystem.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    return entry


@router.get("/", response_model=list[schemas.LifeSupportSystem])
def read_all_entries(db: Session = Depends(get_db)):
    return db.query(models.LifeSupportSystem).all()


@router.put("/{entry_id}", response_model=schemas.LifeSupportSystem)
def update_entry(entry_id: int, updated: schemas.LifeSupportSystemUpdate, db: Session = Depends(get_db)):
    entry = db.query(models.LifeSupportSystem).filter(models.LifeSupportSystem.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    
    for key, value in updated.dict(exclude_unset=True).items():
        setattr(entry, key, value)
    
    db.commit()
    db.refresh(entry)
    return entry


@router.delete("/{entry_id}")
def delete_entry(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(models.LifeSupportSystem).filter(models.LifeSupportSystem.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    
    db.delete(entry)
    db.commit()
    return {"detail": "Entry deleted successfully"}
