from pydantic import BaseModel
from typing import Optional
from datetime import date

class PlanetBase(BaseModel):
    name:str
    description: Optional[str] = None
    distance_from_earth_km: Optional[float] = None
    has_life: Optional[bool] = False
    surface_temperature: Optional[float] = None
    type: Optional[str] = None
    discovered_by: Optional[str] = None
    discovery_date: Optional[date] = None

class PlanetCreate(PlanetBase):
    pass

class PlanetUpdate(PlanetBase):
    pass

class Planet(PlanetBase):
    id: int
    
class config:
    orm_mode = True