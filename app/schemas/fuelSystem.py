from pydantic import BaseModel
from typing import Optional

class FuelBase(BaseModel):
    fuel_level: float
    fuel_consumption_level: float
    fuel_temperature: float
    spacecraft_id: int

class FuelCreate(FuelBase):
    pass

class FuelOut(FuelBase):
    id: int

    class Config:
        orm_mode = True
