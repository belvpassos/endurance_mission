from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import Session
from app.database import get_db
from app import models
from app.schemas import powerSystem as schemas

router = APIRouter(prefix="/power-system", tags=["Power System"])

@router.post("/", response_model=schemas.PowerSystem)
def create_power(entry: schemas.PowerSystemCreate, db: Session = Depends(get_db)):
    new_entry = models.PowerSystem(**entry.dict())
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry

@router.get("/", response_model=schemas.PowerSystem)
def read_power(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(models.PowerSystem).filter(models.PowerSystem.id == entry_id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Power entry not found")
    return entry