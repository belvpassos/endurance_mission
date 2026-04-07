# app/routes/spacecraftStatus.py

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.spacecraftStatus import SpacecraftStatus as Model
from app.schemas import spacecraftStatus as schemas
from app.schemas.common import OperationStatus

router = APIRouter(
    prefix="/spacecraft-status",
    tags=["Spacecraft Status"]
)

@router.post("/", response_model=schemas.SpacecraftStatusResponse, status_code=status.HTTP_201_CREATED)
def create_status(entry: schemas.SpacecraftStatusCreate, db: Session = Depends(get_db)):
    new_entry = Model(**entry.model_dump())
    db.add(new_entry)
    try:
        db.commit()
        db.refresh(new_entry)
        return new_entry
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not create spacecraft status entry: {exc}")

@router.get("/", response_model=list[schemas.SpacecraftStatusResponse])
def read_all_status(db: Session = Depends(get_db)):
    return db.query(Model).all()

@router.get("/{entry_id}", response_model=schemas.SpacecraftStatusResponse)
def read_status(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(Model).filter(Model.id == entry_id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Status not found")
    return entry

@router.put("/{entry_id}", response_model=schemas.SpacecraftStatusResponse)
def update_status(entry_id: int, updated: schemas.SpacecraftStatusUpdate, db: Session = Depends(get_db)):
    entry = db.query(Model).filter(Model.id == entry_id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Status not found")

    for key, value in updated.model_dump(exclude_unset=True).items():
        setattr(entry, key, value)

    try:
        db.commit()
        db.refresh(entry)
        return entry
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not update spacecraft status entry: {exc}")

@router.delete("/{entry_id}", response_model=OperationStatus)
def delete_status(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(Model).filter(Model.id == entry_id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Status not found")

    db.delete(entry)
    try:
        db.commit()
        return OperationStatus(detail="Spacecraft status deleted successfully")
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not delete spacecraft status entry: {exc}")
