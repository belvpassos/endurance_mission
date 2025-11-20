from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import systemHealthCheck as models
from app.schemas import systemHealthCheck as schemas

router = APIRouter(prefix="/system-health-check", tags=["System Health Check"])

@router.post("/", response_model=schemas.SystemHealthCheckResponse)
def create_health_check(entry: schemas.SystemHealthCheckCreate, db: Session = Depends(get_db)):
    new_entry = models.SystemHealthCheck(**entry.dict())
    try:
        db.add(new_entry)
        db.commit()
        db.refresh(new_entry)
    except:
        db.rollback()
        raise
    return new_entry

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
    try:
        for key, value in updated_entry.dict(exclude_unset=True).items():
            setattr(entry, key, value)
        db.commit()
        db.refresh(entry)
    except:
        db.rollback()
        raise
    return entry

@router.delete("/{entry_id}")
def delete_health_check(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(models.SystemHealthCheck).filter(models.SystemHealthCheck.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="System health check not found")
    try:
        db.delete(entry)
        db.commit()
    except:
        db.rollback()
        raise
    return {"detail": "System health check deleted successfully"}
