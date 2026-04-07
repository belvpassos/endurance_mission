from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.thermalControlSystem import ThermalControlSystem
from app.schemas.thermalControlSystem import ThermalControlSystemCreate, ThermalControlSystemUpdate, ThermalControlSystemResponse
from app.schemas.common import OperationStatus

router = APIRouter(prefix="/thermal-control", tags=["Thermal Control System"])

@router.post("/", response_model=ThermalControlSystemResponse, status_code=status.HTTP_201_CREATED)
def create_thermal_system(data: ThermalControlSystemCreate, db: Session = Depends(get_db)):
    try:
        system = ThermalControlSystem(**data.model_dump())
        db.add(system)
        db.commit()
        db.refresh(system)
        return system
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not create thermal system entry: {exc}")

@router.get("/", response_model=list[ThermalControlSystemResponse])
def list_thermal_systems(db: Session = Depends(get_db)):
    return db.query(ThermalControlSystem).all()

@router.get("/{system_id}", response_model=ThermalControlSystemResponse)
def read_thermal_system(system_id: int, db: Session = Depends(get_db)):
    system = db.query(ThermalControlSystem).filter(ThermalControlSystem.id == system_id).first()
    if not system:
        raise HTTPException(status_code=404, detail="Thermal system entry not found")
    return system

@router.put("/{system_id}", response_model=ThermalControlSystemResponse)
def update_thermal_system(system_id: int, updated_data: ThermalControlSystemUpdate, db: Session = Depends(get_db)):
    system = db.query(ThermalControlSystem).filter(ThermalControlSystem.id == system_id).first()
    if not system:
        raise HTTPException(status_code=404, detail="Thermal system entry not found")
    try:
        for key, value in updated_data.model_dump(exclude_unset=True).items():
            setattr(system, key, value)
        db.commit()
        db.refresh(system)
        return system
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not update thermal system entry: {exc}")

@router.delete("/{system_id}", response_model=OperationStatus)
def delete_thermal_system(system_id: int, db: Session = Depends(get_db)):
    system = db.query(ThermalControlSystem).filter(ThermalControlSystem.id == system_id).first()
    if not system:
        raise HTTPException(status_code=404, detail="Thermal system entry not found")
    try:
        db.delete(system)
        db.commit()
        return OperationStatus(detail="Thermal system entry deleted successfully")
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not delete thermal system entry: {exc}")
