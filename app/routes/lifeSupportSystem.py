from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import lifeSupportSystem as models
from app.schemas import lifeSupportSystem as schemas
from app.schemas.common import OperationStatus

router = APIRouter(prefix="/life-support", tags=["Life Support System"])


@router.post("/", response_model=schemas.LifeSupportSystemOut, status_code=status.HTTP_201_CREATED)
def create_entry(entry: schemas.LifeSupportSystemCreate, db: Session = Depends(get_db)):
    new_entry = models.LifeSupportSystem(**entry.model_dump())
    try:
        db.add(new_entry)
        db.commit()
        db.refresh(new_entry)
        return new_entry
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not create life support entry: {exc}")


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

    for key, value in updated.model_dump(exclude_unset=True).items():
        setattr(entry, key, value)

    try:
        db.commit()
        db.refresh(entry)
        return entry
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not update life support entry: {exc}")


@router.delete("/{entry_id}", response_model=OperationStatus)
def delete_entry(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(models.LifeSupportSystem).filter(models.LifeSupportSystem.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")

    try:
        db.delete(entry)
        db.commit()
        return OperationStatus(detail="Life support entry deleted successfully")
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not delete life support entry: {exc}")
