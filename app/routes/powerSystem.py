from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.powerSystem import PowerSystem as PowerSystemModel
from app.schemas.powerSystem import PowerSystem, PowerSystemCreate, PowerSystemUpdate

router = APIRouter(prefix="/power-system", tags=["Power System"])

@router.post("/", response_model=PowerSystem)
def create_power(entry: PowerSystemCreate, db: Session = Depends(get_db)):
    try:
        new_entry = PowerSystemModel(**entry.dict())
        db.add(new_entry)
        db.commit()
        db.refresh(new_entry)
        return new_entry
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating power entry: {e}")

@router.get("/{entry_id}", response_model=PowerSystem)
def read_power(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(PowerSystemModel).filter(PowerSystemModel.id == entry_id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Power entry not found")
    return entry

@router.get("/", response_model=list[PowerSystem])
def read_all_power(db: Session = Depends(get_db)):
    return db.query(PowerSystemModel).all()

@router.put("/{entry_id}", response_model=PowerSystem)
def update_power(entry_id: int, updated: PowerSystemUpdate, db: Session = Depends(get_db)):
    entry = db.query(PowerSystemModel).filter(PowerSystemModel.id == entry_id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Power entry not found")
    
    for key, value in updated.dict(exclude_unset=True).items():
        setattr(entry, key, value)
    
    try:
        db.commit()
        db.refresh(entry)
        return entry
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating power entry: {e}")

@router.delete("/{entry_id}")
def delete_power(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(PowerSystemModel).filter(PowerSystemModel.id == entry_id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Power entry not found")
    
    try:
        db.delete(entry)
        db.commit()
        return {"message": "Entry deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error deleting power entry: {e}")
