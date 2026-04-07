from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import dockingSystem as models
from app.schemas import dockingSystem as schemas
from app.schemas.common import OperationStatus

router = APIRouter(prefix="/docking-system", tags=["Docking System"])

@router.post("/", response_model=schemas.DockingSystem, status_code=status.HTTP_201_CREATED)
def create_docking(entry: schemas.DockingSystemCreate, db: Session = Depends(get_db)):
    try:
        new_entry = models.DockingSystem(**entry.model_dump())
        db.add(new_entry)
        db.commit()
        db.refresh(new_entry)
        return new_entry
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not create docking entry: {exc}")

@router.get("/{entry_id}", response_model=schemas.DockingSystem)
def read_docking(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(models.DockingSystem).filter(models.DockingSystem.id == entry_id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Docking entry not found")
    return entry

@router.get("/", response_model=list[schemas.DockingSystem])
def read_all_docking(db: Session = Depends(get_db)):
    return db.query(models.DockingSystem).all()

@router.put("/{entry_id}", response_model=schemas.DockingSystem)
def update_docking(entry_id: int, updated: schemas.DockingSystemUpdate, db: Session = Depends(get_db)):
    entry = db.query(models.DockingSystem).filter(models.DockingSystem.id == entry_id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Docking entry not found")

    try:
        for key, value in updated.model_dump(exclude_unset=True).items():
            setattr(entry, key, value)
        db.commit()
        db.refresh(entry)
        return entry
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not update docking entry: {exc}")

@router.delete("/{entry_id}", response_model=OperationStatus)
def delete_docking(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(models.DockingSystem).filter(models.DockingSystem.id == entry_id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Docking entry not found")

    try:
        db.delete(entry)
        db.commit()
        return OperationStatus(detail="Docking entry deleted successfully")
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not delete docking entry: {exc}")
