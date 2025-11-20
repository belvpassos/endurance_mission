from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.telemetryData import Telemetry
from app.schemas.telemetryData import TelemetryDataCreate, TelemetryDataResponse, TelemetryDataUpdate

router = APIRouter(prefix="/telemetry", tags=["Telemetry"])

@router.post("/", response_model=TelemetryDataResponse)
def create_telemetry(data: TelemetryDataCreate, db: Session = Depends(get_db)):
    try:
        telemetry = Telemetry(**data.dict())
        db.add(telemetry)
        db.commit()
        db.refresh(telemetry)
        return telemetry
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create telemetry data")

@router.get("/", response_model=list[TelemetryDataResponse])
def list_telemetries(db: Session = Depends(get_db)):
    return db.query(Telemetry).all()

@router.get("/{telemetry_id}", response_model=TelemetryDataResponse)
def read_telemetry(telemetry_id: int, db: Session = Depends(get_db)):
    telemetry = db.query(Telemetry).filter(Telemetry.id == telemetry_id).first()
    if not telemetry:
        raise HTTPException(status_code=404, detail="Telemetry not found")
    return telemetry

@router.put("/{telemetry_id}", response_model=TelemetryDataResponse)
def update_telemetry(telemetry_id: int, updated_data: TelemetryDataUpdate, db: Session = Depends(get_db)):
    telemetry = db.query(Telemetry).filter(Telemetry.id == telemetry_id).first()
    if not telemetry:
        raise HTTPException(status_code=404, detail="Telemetry not found")
    try:
        for key, value in updated_data.dict(exclude_unset=True).items():
            setattr(telemetry, key, value)
        db.commit()
        db.refresh(telemetry)
        return telemetry
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update telemetry data")

@router.delete("/{telemetry_id}")
def delete_telemetry(telemetry_id: int, db: Session = Depends(get_db)):
    telemetry = db.query(Telemetry).filter(Telemetry.id == telemetry_id).first()
    if not telemetry:
        raise HTTPException(status_code=404, detail="Telemetry not found")
    try:
        db.delete(telemetry)
        db.commit()
        return {"detail": "Telemetry data deleted successfully"}
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete telemetry data")
