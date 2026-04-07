from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import commandQueue as models
from app.schemas import commandQueue as schemas
from app.schemas.common import OperationStatus

router = APIRouter(prefix="/command-queue", tags=["Command Queue"])

@router.post("/", response_model=schemas.CommandQueue, status_code=status.HTTP_201_CREATED)
def create_command(entry: schemas.CommandQueueCreate, db: Session = Depends(get_db)):
    try:
        new_entry = models.CommandQueue(**entry.model_dump())
        db.add(new_entry)
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
        for key, value in updated.model_dump(exclude_unset=True).items():
            setattr(entry, key, value)
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
