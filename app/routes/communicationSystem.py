from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import communicationSystem as models
from app.schemas import communicationSystem as schemas
from app.schemas.common import OperationStatus

router = APIRouter(prefix="/communication", tags=["Communication System"])

@router.post("/", response_model=schemas.Communication, status_code=status.HTTP_201_CREATED)
def create_communication(entry: schemas.CommunicationCreate, db: Session = Depends(get_db)):
    try:
        new_entry = models.CommunicationSystem(**entry.model_dump())
        db.add(new_entry)
        db.commit()
        db.refresh(new_entry)
        return new_entry
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not create communication entry: {exc}")

@router.get("/{entry_id}", response_model=schemas.Communication)
def read_communication(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(models.CommunicationSystem).filter(models.CommunicationSystem.id == entry_id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Communication entry not found")
    return entry

@router.get("/", response_model=list[schemas.Communication])
def read_all_communication(db: Session = Depends(get_db)):
    return db.query(models.CommunicationSystem).all()

@router.put("/{entry_id}", response_model=schemas.Communication)
def update_communication(entry_id: int, updated: schemas.CommunicationUpdate, db: Session = Depends(get_db)):
    entry = db.query(models.CommunicationSystem).filter(models.CommunicationSystem.id == entry_id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Communication entry not found")
    try:
        for key, value in updated.model_dump(exclude_unset=True).items():
            setattr(entry, key, value)
        db.commit()
        db.refresh(entry)
        return entry
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not update communication entry: {exc}")

@router.delete("/{entry_id}", response_model=OperationStatus)
def delete_communication(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(models.CommunicationSystem).filter(models.CommunicationSystem.id == entry_id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Communication entry not found")
    try:
        db.delete(entry)
        db.commit()
        return OperationStatus(detail="Communication entry deleted successfully")
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not delete communication entry: {exc}")
