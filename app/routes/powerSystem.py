from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.powerSystem import PowerSystem as PowerSystemModel
from app.schemas.powerSystem import PowerSystem, PowerSystemCreate, PowerSystemUpdate
from app.schemas.common import OperationStatus

router = APIRouter(prefix="/power-system", tags=["Power System"])

@router.post("/", response_model=PowerSystem, status_code=status.HTTP_201_CREATED)
def create_power(entry: PowerSystemCreate, db: Session = Depends(get_db)):
    try:
        new_entry = PowerSystemModel(**entry.model_dump())
        db.add(new_entry)
        db.commit()
        db.refresh(new_entry)
        return new_entry
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not create power entry: {exc}")

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

    for key, value in updated.model_dump(exclude_unset=True).items():
        setattr(entry, key, value)

    try:
        db.commit()
        db.refresh(entry)
        return entry
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not update power entry: {exc}")

@router.delete("/{entry_id}", response_model=OperationStatus)
def delete_power(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(PowerSystemModel).filter(PowerSystemModel.id == entry_id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Power entry not found")
    
    try:
        db.delete(entry)
        db.commit()
        return OperationStatus(detail="Power entry deleted successfully")
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not delete power entry: {exc}")
