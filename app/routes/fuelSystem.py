from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.fuelSystem import Fuel
from app.schemas.fuelSystem import FuelCreate, FuelOut
from app.database import get_db
from app.schemas.common import OperationStatus

router = APIRouter(prefix="/fuel", tags=["Fuel System"])


@router.post("/", response_model=FuelOut, status_code=status.HTTP_201_CREATED)
def create_fuel(data: FuelCreate, db: Session = Depends(get_db)):
    try:
        fuel = Fuel(**data.model_dump())
        db.add(fuel)
        db.commit()
        db.refresh(fuel)
        return fuel
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not create fuel entry: {exc}")


@router.get("/", response_model=list[FuelOut])
def read_all_fuel(db: Session = Depends(get_db)):
    return db.query(Fuel).all()


@router.get("/{id}", response_model=FuelOut)
def read_fuel(id: int, db: Session = Depends(get_db)):
    fuel = db.query(Fuel).filter(Fuel.id == id).first()
    if not fuel:
        raise HTTPException(status_code=404, detail="Fuel not found")
    return fuel


@router.put("/{id}", response_model=FuelOut)
def update_fuel(id: int, data: FuelCreate, db: Session = Depends(get_db)):
    fuel = db.query(Fuel).filter(Fuel.id == id).first()
    if not fuel:
        raise HTTPException(status_code=404, detail="Fuel not found")
    try:
        for key, value in data.model_dump().items():
            setattr(fuel, key, value)
        db.commit()
        db.refresh(fuel)
        return fuel
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not update fuel entry: {exc}")


@router.delete("/{id}", response_model=OperationStatus)
def delete_fuel(id: int, db: Session = Depends(get_db)):
    fuel = db.query(Fuel).filter(Fuel.id == id).first()
    if not fuel:
        raise HTTPException(status_code=404, detail="Fuel not found")
    try:
        db.delete(fuel)
        db.commit()
        return OperationStatus(detail="Fuel entry deleted successfully")
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not delete fuel entry: {exc}")
