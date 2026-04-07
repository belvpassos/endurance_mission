from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.models.groundControlLog import GroundControlLog
from app.schemas.groundControlLog import GroundControlLogCreate, GroundControlLogOut, GroundControlLogUpdate
from app.database import get_db
from app.schemas.common import OperationStatus

router = APIRouter(prefix="/ground-control-log", tags=["Ground Control Log"])

@router.post("/", response_model=GroundControlLogOut, status_code=status.HTTP_201_CREATED)
def create_log(data: GroundControlLogCreate, db: Session = Depends(get_db)):
    try:
        log = GroundControlLog(**data.model_dump())
        db.add(log)
        db.commit()
        db.refresh(log)
        return log
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not create ground control log entry: {exc}")

@router.get("/", response_model=list[GroundControlLogOut])
def read_all_logs(db: Session = Depends(get_db)):
    return db.query(GroundControlLog).all()

@router.get("/{id}", response_model=GroundControlLogOut)
def read_log(id: int, db: Session = Depends(get_db)):
    log = db.query(GroundControlLog).filter(GroundControlLog.id == id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
    return log

@router.put("/{id}", response_model=GroundControlLogOut)
def update_log(id: int, data: GroundControlLogUpdate, db: Session = Depends(get_db)):
    log = db.query(GroundControlLog).filter(GroundControlLog.id == id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
    try:
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(log, key, value)
        db.commit()
        db.refresh(log)
        return log
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not update ground control log entry: {exc}")

@router.delete("/{id}", response_model=OperationStatus)
def delete_log(id: int, db: Session = Depends(get_db)):
    log = db.query(GroundControlLog).filter(GroundControlLog.id == id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
    try:
        db.delete(log)
        db.commit()
        return OperationStatus(detail="Ground control log deleted successfully")
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not delete ground control log entry: {exc}")
