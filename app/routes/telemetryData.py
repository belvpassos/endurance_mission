from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.telemetryData import Telemetry
from app.schemas.telemetryData import TelemetryDataCreate, TelemetryDataResponse

router = APIRouter(prefix="/telemetry", tags=["Telemetry"])

@router.post("/", response_model = TelemetryDataResponse)
def create_telemetry(data: TelemetryDataCreate, db: Session = Depends(get_db)):
    telemetry = Telemetry(**data.dict())
    db.add(telemetry)
    db.commit()
    db.refresh(telemetry)
    return telemetry

@router.get("/{telemetry_id}", response_model=TelemetryDataResponse)
def read_telemetru(telemetry_id: int, db: Session = Depends(get_db)):
    telemetry = db.query(Telemetry).filter(Telemetry.id == telemetry_id).first()
    if not telemetry:
        raise HTTPException(status_code=404, detail="Telemetry not found")
    return telemetry

@router.get("/", response_model=list[TelemetryDataResponse])
def list_telemetries(db: Session = Depends(get_db)):
    return db.query(Telemetry).all()