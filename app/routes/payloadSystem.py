from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import payloadSystem as models
from app.schemas import payloadSystem as schemas
from app.schemas.common import OperationStatus

router = APIRouter(prefix="/payload-system", tags=["Payload System"])


@router.post("/", response_model=schemas.PayloadSystem, status_code=status.HTTP_201_CREATED)
def create_payload(entry: schemas.PayloadSystemCreate, db: Session = Depends(get_db)):
    new_entry = models.PayloadSystem(**entry.model_dump())
    try:
        db.add(new_entry)
        db.commit()
        db.refresh(new_entry)
        return new_entry
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not create payload entry: {exc}")


@router.get("/{entry_id}", response_model=schemas.PayloadSystem)
def read_payload(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(models.PayloadSystem).filter(models.PayloadSystem.id == entry_id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Payload entry not found")
    return entry


@router.get("/", response_model=list[schemas.PayloadSystem])
def read_all_payload(db: Session = Depends(get_db)):
    return db.query(models.PayloadSystem).all()


@router.put("/{entry_id}", response_model=schemas.PayloadSystem)
def update_payload(entry_id: int, updated: schemas.PayloadSystemUpdate, db: Session = Depends(get_db)):
    entry = db.query(models.PayloadSystem).filter(models.PayloadSystem.id == entry_id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Payload entry not found")

    for key, value in updated.model_dump(exclude_unset=True).items():
        setattr(entry, key, value)

    try:
        db.commit()
        db.refresh(entry)
        return entry
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not update payload entry: {exc}")


@router.delete("/{entry_id}", response_model=OperationStatus)
def delete_payload(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(models.PayloadSystem).filter(models.PayloadSystem.id == entry_id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Payload entry not found")

    try:
        db.delete(entry)
        db.commit()
        return OperationStatus(detail="Payload entry deleted successfully")
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not delete payload entry: {exc}")
