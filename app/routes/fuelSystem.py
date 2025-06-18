from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.fuelSystem import Fuel
from app.schemas.fuelSystem import FuelCreate, FuelOut
from app.database import get_db

router = APIRouter()

@router.post("/", response_model=FuelOut)
def create_fuel(data: FuelCreate, db: Session = Depends(get_db)):
    fuel = Fuel(**data.dict())
    db.add(fuel)
    db.commit()
    db.refresh(fuel)
    return fuel

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
    for key, value in data.dict().items():
        setattr(fuel, key, value)
    db.commit()
    db.refresh(fuel)
    return fuel

@router.delete("/{id}")
def delete_fuel(id: int, db: Session = Depends(get_db)):
    fuel = db.query(Fuel).filter(Fuel.id == id).first()
    if not fuel:
        raise HTTPException(status_code=404, detail="Fuel not found")
    db.delete(fuel)
    db.commit()
    return {"detail":"Fuel deleted"}