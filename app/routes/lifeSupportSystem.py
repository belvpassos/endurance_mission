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
    entry = db.query(models.LifeSupportSystem).filter(models.lifeSupportSystem.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    return entry
