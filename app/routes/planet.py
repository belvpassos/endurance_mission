from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing  import List

from app.models.planet import Planet as PlanetModel


from app.database import get_db
from app.models.planet import Planet
from app.schemas.planet import Planet, PlanetCreate, PlanetUpdate

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

@router.put("/", response_model = Planet)
def create_planet(planet: PlanetCreate, db: Session = Depends(get_db)):
    new_planet = PlanetModel(**planet.dict())
    db.add(new_planet)
    db.commit()
    db.refresh(new_planet)
    return  new_planet

@router.put("/{planet_id}", response_model=Planet)
def update_planet(planet_id: int, updated_planet: PlanetUpdate, db: Session = Depends(get_db)):
    planet = db.query(PlanetModel).filter(PlanetModel.id == planet_id).first()
    if planet is None:
        raise HTTPException(status_code=400, detail="Planet not found")
    
    for key, value in updated_planet.dict(exclude_unset=True).items():
        setattr(planet, key, value)
    
    db.commit()
    db.refresh(planet)
    return planet

@router.delete("/planet_id")
def delete_planet(planet_id: int, db: Session = Depends(get_db)):
    planet = db.query(PlanetModel).filter(PlanetModel.id == planet_id).first()
    if planet is None:
        raise HTTPException(status_code=404, detail="Planet not found")
    
    db.delete(planet)
    db.commit
    return{"detail": "Planet deleted successfully"}