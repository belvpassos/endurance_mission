from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.database import get_db
from app.models import navigationSystem as models
from app.schemas import navigationSystem as schemas
from app.schemas.common import OperationStatus

router = APIRouter(prefix="/navigation-system", tags=["Navigation System"])


@router.post("/", response_model=schemas.NavigationSystem, status_code=status.HTTP_201_CREATED)
def create_navigation(entry: schemas.NavigationSystemCreate, db: Session = Depends(get_db)):
    new_entry = models.NavigationSystem(**entry.model_dump())
    try:
        db.add(new_entry)
        db.commit()
        db.refresh(new_entry)
        return new_entry
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not create navigation entry: {exc}")


@router.get("/{entry_id}", response_model=schemas.NavigationSystem)
def read_navigation(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(models.NavigationSystem).filter(models.NavigationSystem.id == entry_id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Navigation entry not found")
    return entry


@router.get("/", response_model=list[schemas.NavigationSystem])
def read_all_navigation(db: Session = Depends(get_db)):
    return db.query(models.NavigationSystem).all()


@router.put("/{entry_id}", response_model=schemas.NavigationSystem)
def update_navigation(entry_id: int, updated: schemas.NavigationSystemUpdate, db: Session = Depends(get_db)):
    entry = db.query(models.NavigationSystem).filter(models.NavigationSystem.id == entry_id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Navigation entry not found")

    for key, value in updated.model_dump(exclude_unset=True).items():
        setattr(entry, key, value)

    try:
        db.commit()
        db.refresh(entry)
        return entry
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not update navigation entry: {exc}")


@router.delete("/{entry_id}", response_model=OperationStatus)
def delete_navigation(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(models.NavigationSystem).filter(models.NavigationSystem.id == entry_id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Navigation entry not found")

    try:
        db.delete(entry)
        db.commit()
        return OperationStatus(detail="Navigation entry deleted successfully")
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not delete navigation entry: {exc}")
