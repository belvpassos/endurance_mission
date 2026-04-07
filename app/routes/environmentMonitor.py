from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.environmentMonitor import EnvironmentMonitor
from app.schemas.environmentMonitor import (
    EnvironmentMonitorCreate,
    EnvironmentMonitorUpdate,
    EnvironmentMonitorInDB,
)
from app.schemas.common import OperationStatus

router = APIRouter(prefix="/environment", tags=["Environment Monitor"])

@router.post("/", response_model=EnvironmentMonitorInDB, status_code=status.HTTP_201_CREATED)
def create_environment_data(
    data: EnvironmentMonitorCreate, db: Session = Depends(get_db)
):
    try:
        env = EnvironmentMonitor(**data.model_dump())
        db.add(env)
        db.commit()
        db.refresh(env)
        return env
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not create environment data: {exc}")

@router.get("/{env_id}", response_model=EnvironmentMonitorInDB)
def read_environment_data(env_id: int, db: Session = Depends(get_db)):
    env = db.query(EnvironmentMonitor).filter(EnvironmentMonitor.id == env_id).first()
    if not env:
        raise HTTPException(status_code=404, detail="Environment data not found")
    return env

@router.put("/{env_id}", response_model=EnvironmentMonitorInDB)
def update_environment_data(
    env_id: int,
    data: EnvironmentMonitorUpdate,
    db: Session = Depends(get_db)
):
    env = db.query(EnvironmentMonitor).filter(EnvironmentMonitor.id == env_id).first()
    if not env:
        raise HTTPException(status_code=404, detail="Environment data not found")

    try:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(env, field, value)
        db.commit()
        db.refresh(env)
        return env
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not update environment data: {exc}")

@router.delete("/{env_id}", response_model=OperationStatus)
def delete_environment_data(env_id: int, db: Session = Depends(get_db)):
    env = db.query(EnvironmentMonitor).filter(EnvironmentMonitor.id == env_id).first()
    if not env:
        raise HTTPException(status_code=404, detail="Environment data not found")
    try:
        db.delete(env)
        db.commit()
        return OperationStatus(detail="Environment data deleted successfully")
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not delete environment data: {exc}")
