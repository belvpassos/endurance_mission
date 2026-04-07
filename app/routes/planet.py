from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.planet import Planet as PlanetModel
from app.schemas.planet import Planet, PlanetCreate, PlanetUpdate
from app.schemas.common import OperationStatus

router = APIRouter(prefix="/planets", tags=["Planets"])


@router.get("/", response_model=List[Planet])
def get_all_planets(db: Session = Depends(get_db)):
    return db.query(PlanetModel).all()


@router.get("/{planet_id}", response_model=Planet)
def get_planet(planet_id: int, db: Session = Depends(get_db)):
    planet = db.query(PlanetModel).filter(PlanetModel.id == planet_id).first()
    if planet is None:
        raise HTTPException(status_code=404, detail="Planet not found")
    return planet


@router.post("/", response_model=Planet, status_code=status.HTTP_201_CREATED)
def create_planet(planet: PlanetCreate, db: Session = Depends(get_db)):
    new_planet = PlanetModel(**planet.model_dump())
    try:
        db.add(new_planet)
        db.commit()
        db.refresh(new_planet)
        return new_planet
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not create planet: {exc}")


@router.put("/{planet_id}", response_model=Planet)
def update_planet(planet_id: int, updated_planet: PlanetUpdate, db: Session = Depends(get_db)):
    planet = db.query(PlanetModel).filter(PlanetModel.id == planet_id).first()
    if planet is None:
        raise HTTPException(status_code=404, detail="Planet not found")

    for key, value in updated_planet.model_dump(exclude_unset=True).items():
        setattr(planet, key, value)

    try:
        db.commit()
        db.refresh(planet)
        return planet
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not update planet: {exc}")


@router.delete("/{planet_id}", response_model=OperationStatus)
def delete_planet(planet_id: int, db: Session = Depends(get_db)):
    planet = db.query(PlanetModel).filter(PlanetModel.id == planet_id).first()
    if planet is None:
        raise HTTPException(status_code=404, detail="Planet not found")

    try:
        db.delete(planet)
        db.commit()
        return OperationStatus(detail="Planet deleted successfully")
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not delete planet: {exc}")
