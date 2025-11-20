from pydantic import BaseModel
from typing import Optional
from datetime import date


class PlanetBase(BaseModel):
    name: str
    description: Optional[str] = None
    type: str
    distance_from_earth_km: float
    has_life: Optional[bool] = False
    surface_temperature: Optional[float] = None
    discovered_by: Optional[str] = None
    discovery_date: Optional[date] = None
    gravity: Optional[float] = None
    atmosphere: Optional[str] = None
    habitability_score: Optional[float] = None


class PlanetCreate(PlanetBase):
    pass


class PlanetUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    distance_from_earth_km: Optional[float] = None
    has_life: Optional[bool] = None
    surface_temperature: Optional[float] = None
    discovered_by: Optional[str] = None
    discovery_date: Optional[date] = None
    gravity: Optional[float] = None
    atmosphere: Optional[str] = None
    habitability_score: Optional[float] = None


class Planet(PlanetBase):
    id: int

    class Config:
        from_attributes = True
