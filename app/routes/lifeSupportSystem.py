from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import lifeSupportSystem as models
from app.schemas import lifeSupportSystem as schemas

router = APIRouter(prefix="/life-support", tags=["Life Support System"])

@router.post("/", response_model=schemas.LifeSupportSystemOut)
def create_entry(entry: schemas.LifeSupportSystemCreate, db: Session = Depends(get_db)):
    new_entry = models.LifeSupportSystem(**entry.dict())
    try:
        db.add(new_entry)
        db.commit()
        db.refresh(new_entry)
    except:
        db.rollback()
        raise
    return new_entry

@router.get("/{entry_id}", response_model=schemas.LifeSupportSystemOut)
def read_entry(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(models.LifeSupportSystem).filter(models.LifeSupportSystem.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    return entry

@router.get("/", response_model=list[schemas.LifeSupportSystemOut])
def read_all_entries(db: Session = Depends(get_db)):
    return db.query(models.LifeSupportSystem).all()

@router.put("/{entry_id}", response_model=schemas.LifeSupportSystemOut)
def update_entry(entry_id: int, updated: schemas.LifeSupportSystemUpdate, db: Session = Depends(get_db)):
    entry = db.query(models.LifeSupportSystem).filter(models.LifeSupportSystem.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    
    for key, value in updated.dict(exclude_unset=True).items():
        setattr(entry, key, value)
    
    try:
        db.commit()
        db.refresh(entry)
    except:
        db.rollback()
        raise
    
    return entry

@router.delete("/{entry_id}")
def delete_entry(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(models.LifeSupportSystem).filter(models.LifeSupportSystem.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    
    try:
        db.delete(entry)
        db.commit()
    except:
        db.rollback()
        raise
    
    return {"detail": "Entry deleted successfully"}
