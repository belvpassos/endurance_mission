from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ResourceManagementBase(BaseModel):
    power_avaliable: float
    fuel_remaining: float
    water_reserve: float
    oxygen_level: float
    co2_level: float
    food_suplies: float
    average_consumption_rate: float
    projected_depletion_date: datetime
    power_critical: bool
    fuel_critical: bool
    water_critical: bool
    oxygen_critical: bool
    food_critical: bool
    last_update: datetime

class ResourceManagementCreate(ResourceManagementBase):
    spacecraft_id: int

class ResourceManagementUpdate(ResourceManagementBase):
    power_avaliable: Optional[float] = None
    fuel_remaining: Optional[float] = None
    water_reserve: Optional[float] = None
    oxygen_level: Optional[float] = None
    co2_level: Optional[float] = None
    food_suplies: Optional[float] = None
    average_consumption_rate: Optional[float] = None
    projected_depletion_date: Optional[datetime] = None
    power_critical: Optional[bool] = None
    fuel_critical: Optional[bool] = None
    water_critical: Optional[bool] = None
    oxygen_critical: Optional[bool] = None
    food_critical: Optional[bool] = None
    last_update: Optional[datetime] = None

class ResourceManagement(ResourceManagementBase):
    id: int
    spacecraft_id:int
    
    class Config:
        from_attributes: True