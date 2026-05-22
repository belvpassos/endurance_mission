from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import commandQueue as models
from app.models.missionEvents import EventType, MissionEvent
from app.schemas import commandQueue as schemas
from app.schemas.common import OperationStatus

router = APIRouter(prefix="/command-queue", tags=["Command Queue"])


def _status_value(status: object) -> str:
    return status.value if hasattr(status, "value") else str(status)


def _normalize_command_state(entry: models.CommandQueue) -> None:
    current_status = _status_value(entry.status)
    if current_status == models.CommandStatus.EXECUTING.value:
        entry.executed = False
        entry.executed_time = None
    elif current_status == models.CommandStatus.CONFIRMED.value:
        entry.executed = True
        entry.executed_time = entry.executed_time or datetime.utcnow()
    elif current_status in {models.CommandStatus.FAILED.value, models.CommandStatus.ABORTED.value}:
        entry.executed = False
        entry.executed_time = entry.executed_time or datetime.utcnow()
    else:
        entry.executed = False
        entry.executed_time = None


def _log_command_event(db: Session, entry: models.CommandQueue, event_type: EventType, description: str) -> None:
    db.add(
        MissionEvent(
            event_type=event_type,
            timestamp=datetime.utcnow(),
            description=description,
            spacecraft_id=entry.spacecraft_id,
        )
    )


def _describe_parameters(parameters: str | None) -> str:
    return parameters if parameters else "no parameters"


@router.post("/", response_model=schemas.CommandQueue, status_code=status.HTTP_201_CREATED)
def create_command(entry: schemas.CommandQueueCreate, db: Session = Depends(get_db)):
    try:
        new_entry = models.CommandQueue(**entry.model_dump())
        _normalize_command_state(new_entry)
        db.add(new_entry)
        db.flush()
        _log_command_event(
            db,
            new_entry,
            EventType.COMMAND_UPLINK,
            f"Command uplink queued: {new_entry.command} with {_describe_parameters(new_entry.parameters)}.",
        )
        db.commit()
        db.refresh(new_entry)
        return new_entry
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not create command queue entry: {exc}")

@router.get("/{entry_id}", response_model=schemas.CommandQueue)
def read_command(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(models.CommandQueue).filter(models.CommandQueue.id == entry_id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Command not found")
    return entry

@router.get("/", response_model=list[schemas.CommandQueue])
def read_all_commands(db: Session = Depends(get_db)):
    return db.query(models.CommandQueue).all()

@router.put("/{entry_id}", response_model=schemas.CommandQueue)
def update_command(entry_id: int, updated: schemas.CommandQueueUpdate, db: Session = Depends(get_db)):
    entry = db.query(models.CommandQueue).filter(models.CommandQueue.id == entry_id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Command not found")
    try:
        previous_status = _status_value(entry.status)
        for key, value in updated.model_dump(exclude_unset=True).items():
            setattr(entry, key, value)
        _normalize_command_state(entry)
        current_status = _status_value(entry.status)
        if current_status != previous_status:
            if current_status == models.CommandStatus.EXECUTING.value:
                _log_command_event(
                    db,
                    entry,
                    EventType.COMMAND_EXECUTING,
                    f"Command execution started: {entry.command}.",
                )
            elif current_status == models.CommandStatus.CONFIRMED.value:
                _log_command_event(
                    db,
                    entry,
                    EventType.COMMAND_CONFIRMED,
                    f"Command confirmed: {entry.command} completed successfully.",
                )
            elif current_status in {models.CommandStatus.FAILED.value, models.CommandStatus.ABORTED.value}:
                _log_command_event(
                    db,
                    entry,
                    EventType.COMMAND_FAILED,
                    f"Command {entry.command} ended with status {current_status}.",
                )
        db.commit()
        db.refresh(entry)
        return entry
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not update command queue entry: {exc}")

@router.delete("/{entry_id}", response_model=OperationStatus)
def delete_command(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(models.CommandQueue).filter(models.CommandQueue.id == entry_id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Command not found")
    try:
        db.delete(entry)
        db.commit()
        return OperationStatus(detail="Command queue entry deleted successfully")
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not delete command queue entry: {exc}")
