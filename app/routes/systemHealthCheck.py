from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import systemHealthCheck as models
from app.schemas import systemHealthCheck as schemas
from app.schemas.common import OperationStatus

router = APIRouter(prefix="/system-health-check", tags=["System Health Check"])


@router.post("/", response_model=schemas.SystemHealthCheckResponse, status_code=status.HTTP_201_CREATED)
def create_health_check(entry: schemas.SystemHealthCheckCreate, db: Session = Depends(get_db)):
    new_entry = models.SystemHealthCheck(**entry.model_dump())
    try:
        db.add(new_entry)
        db.commit()
        db.refresh(new_entry)
        return new_entry
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not create system health check entry: {exc}")


@router.get("/", response_model=list[schemas.SystemHealthCheckResponse])
def read_all_health_checks(db: Session = Depends(get_db)):
    return db.query(models.SystemHealthCheck).all()


@router.get("/{entry_id}", response_model=schemas.SystemHealthCheckResponse)
def read_health_check(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(models.SystemHealthCheck).filter(models.SystemHealthCheck.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="System health check not found")
    return entry


@router.put("/{entry_id}", response_model=schemas.SystemHealthCheckResponse)
def update_health_check(entry_id: int, updated_entry: schemas.SystemHealthCheckUpdate, db: Session = Depends(get_db)):
    entry = db.query(models.SystemHealthCheck).filter(models.SystemHealthCheck.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="System health check not found")

    for key, value in updated_entry.model_dump(exclude_unset=True).items():
        setattr(entry, key, value)

    try:
        db.commit()
        db.refresh(entry)
        return entry
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not update system health check entry: {exc}")


@router.delete("/{entry_id}", response_model=OperationStatus)
def delete_health_check(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(models.SystemHealthCheck).filter(models.SystemHealthCheck.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="System health check not found")

    try:
        db.delete(entry)
        db.commit()
        return OperationStatus(detail="System health check deleted successfully")
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not delete system health check entry: {exc}")
