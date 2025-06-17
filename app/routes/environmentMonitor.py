from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.environmentMonitor import EnvironmentMonitor
from app.schemas.environmentMonitor import (
    EnvironmentMonitorCreate,
    EnvironmentMonitorUpdate,
    EnvironmentMonitorInDB,
)

router = APIRouter(prefix="/environment", tags=["Environment Monitor"])

@router.post("/", response_model=EnvironmentMonitorInDB)
def create_environment_data(
    data: EnvironmentMonitorCreate, db: Session = Depends(get_db)
):
    env = EnvironmentMonitor(**data.dict())
    db.add(env)
    db.commit()
    db.refresh(env)
    return env

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

    for field, value in data.dict(exclude_unset=True).items():
        setattr(env, field, value)

    db.commit()
    db.refresh(env)
    return env

@router.delete("/{env_id}")
def delete_environment_data(env_id: int, db: Session = Depends(get_db)):
    env = db.query(EnvironmentMonitor).filter(EnvironmentMonitor.id == env_id).first()
    if not env:
        raise HTTPException(status_code=404, detail="Environment data not found")
    db.delete(env)
    db.commit()
    return {"detail": "Deleted successfully"}
