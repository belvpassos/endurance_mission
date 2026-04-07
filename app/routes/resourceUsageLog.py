from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from app.database import get_db
from app.models.resourceUsageLog import ResourceUsageLog as ResourceUsageLogModel
from app.schemas.resourceUsageLog import (
    ResourceUsageLog,
    ResourceUsageLogCreate,
    ResourceUsageLogUpdate
)
from app.schemas.common import OperationStatus

router = APIRouter(prefix="/resource-usage-log", tags=["Resource Usage Log"])


# ------------------
# Create Log
# ------------------
@router.post("/", response_model=ResourceUsageLog, status_code=status.HTTP_201_CREATED)
def create_log(entry: ResourceUsageLogCreate, db: Session = Depends(get_db)):
    try:
        new_entry = ResourceUsageLogModel(**entry.model_dump())
        db.add(new_entry)
        db.commit()
        db.refresh(new_entry)
        return new_entry

    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not create resource usage log entry: {exc}")



# ------------------
# Read log by ID
# ------------------
@router.get("/{entry_id}", response_model=ResourceUsageLog)
def read_log(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(ResourceUsageLogModel).filter(ResourceUsageLogModel.id == entry_id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Log entry not found")
    return entry



# ------------------
# Read all logs
# ------------------
@router.get("/", response_model=list[ResourceUsageLog])
def read_all_logs(db: Session = Depends(get_db)):
    return db.query(ResourceUsageLogModel).order_by(ResourceUsageLogModel.timestamp.desc()).all()



# ------------------
# Update log
# ------------------
@router.put("/{entry_id}", response_model=ResourceUsageLog)
def update_log(entry_id: int, updated: ResourceUsageLogUpdate, db: Session = Depends(get_db)):
    entry = db.query(ResourceUsageLogModel).filter(ResourceUsageLogModel.id == entry_id).first()

    if entry is None:
        raise HTTPException(status_code=404, detail="Log entry not found")

    try:
        for key, value in updated.model_dump(exclude_unset=True).items():
            setattr(entry, key, value)

        db.commit()
        db.refresh(entry)
        return entry

    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not update resource usage log entry: {exc}")



# ------------------
# Delete log
# ------------------
@router.delete("/{entry_id}", response_model=OperationStatus)
def delete_log(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(ResourceUsageLogModel).filter(ResourceUsageLogModel.id == entry_id).first()

    if entry is None:
        raise HTTPException(status_code=404, detail="Log entry not found")

    try:
        db.delete(entry)
        db.commit()
        return OperationStatus(detail="Resource usage log entry deleted successfully")

    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not delete resource usage log entry: {exc}")



# =====================================================
# EXTRA ENDPOINTS (Impressionam recrutadores)
# =====================================================


# 1. Logs por tipo de recurso
@router.get("/resource/{resource_type}", response_model=list[ResourceUsageLog])
def get_logs_by_resource(resource_type: str, db: Session = Depends(get_db)):
    return (
        db.query(ResourceUsageLogModel)
        .filter(ResourceUsageLogModel.resource_type == resource_type)
        .order_by(ResourceUsageLogModel.timestamp.desc())
        .all()
    )


# 2. Logs por espaçonave
@router.get("/spacecraft/{spacecraft_id}", response_model=list[ResourceUsageLog])
def get_logs_by_spacecraft(spacecraft_id: int, db: Session = Depends(get_db)):
    return (
        db.query(ResourceUsageLogModel)
        .filter(ResourceUsageLogModel.spacecraft_id == spacecraft_id)
        .order_by(ResourceUsageLogModel.timestamp.desc())
        .all()
    )


# 3. Logs recentes (telemetria ao vivo)
@router.get("/recent/", response_model=list[ResourceUsageLog])
def get_recent_logs(limit: int = 50, db: Session = Depends(get_db)):
    return (
        db.query(ResourceUsageLogModel)
        .order_by(ResourceUsageLogModel.timestamp.desc())
        .limit(limit)
        .all()
    )


# 4. Logs por intervalo de datas
@router.get("/range/", response_model=list[ResourceUsageLog])
def get_logs_in_range(start: datetime, end: datetime, db: Session = Depends(get_db)):
    return (
        db.query(ResourceUsageLogModel)
        .filter(ResourceUsageLogModel.timestamp >= start)
        .filter(ResourceUsageLogModel.timestamp <= end)
        .order_by(ResourceUsageLogModel.timestamp.asc())
        .all()
    )
