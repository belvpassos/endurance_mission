from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import missionEvents as models
from app.schemas import missionEvents as schemas
from app.schemas.common import OperationStatus
from app.services.missionState import sync_latest_mission_phase_from_event

router = APIRouter(prefix="/mission-events", tags=["Mission Events"])

@router.post("/", response_model=schemas.MissionEvent, status_code=status.HTTP_201_CREATED)
def create_mission_event(event: schemas.MissionEventCreate, db: Session = Depends(get_db)):
    try:
        new_event = models.MissionEvent(**event.model_dump())
        db.add(new_event)
        db.flush()
        sync_latest_mission_phase_from_event(db, new_event)
        db.commit()
        db.refresh(new_event)
        return new_event
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not create mission event: {exc}")

@router.get("/", response_model=list[schemas.MissionEvent])
def read_all_events(db: Session = Depends(get_db)):
    return db.query(models.MissionEvent).all()

@router.get("/{event_id}", response_model=schemas.MissionEvent)
def read_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(models.MissionEvent).filter(models.MissionEvent.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.put("/{event_id}", response_model=schemas.MissionEvent)
def update_event(event_id: int, updated: schemas.MissionEventUpdate, db: Session = Depends(get_db)):
    event = db.query(models.MissionEvent).filter(models.MissionEvent.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    try:
        for key, value in updated.model_dump(exclude_unset=True).items():
            setattr(event, key, value)
        sync_latest_mission_phase_from_event(db, event)
        db.commit()
        db.refresh(event)
        return event
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not update mission event: {exc}")

@router.delete("/{event_id}", response_model=OperationStatus)
def delete_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(models.MissionEvent).filter(models.MissionEvent.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    try:
        db.delete(event)
        db.commit()
        return OperationStatus(detail="Mission event deleted successfully")
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not delete mission event: {exc}")
