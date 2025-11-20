from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import missionEvents as models
from app.schemas import missionEvents as schemas

router = APIRouter(prefix="/mission-events", tags=["Mission Events"])

@router.post("/", response_model=schemas.MissionEvent)
def create_mission_event(event: schemas.MissionEventCreate, db: Session = Depends(get_db)):
    try:
        new_event = models.MissionEvent(**event.dict())
        db.add(new_event)
        db.commit()
        db.refresh(new_event)
        return new_event
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

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
        for key, value in updated.dict(exclude_unset=True).items():
            setattr(event, key, value)
        db.commit()
        db.refresh(event)
        return event
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{event_id}")
def delete_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(models.MissionEvent).filter(models.MissionEvent.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    try:
        db.delete(event)
        db.commit()
        return {"message": "Event deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
