from pydantic import BaseModel
from typing import Optional

class PropulsionSystemBase(BaseModel):
    thrust_level: float
    fuel_flow_rate: float
    engine_status: str
    active_engine: str
    emergency_shutdown: bool

class PropulsionSystemCreate(PropulsionSystemBase):
    spacecraft_id: int

class PropulsionSystemUpdate(PropulsionSystemBase):
    thrust_level: Optional[float] = None
    fuel_flow_rate: Optional[float] = None
    engine_status: Optional[str] =  None
    active_engine: Optional[str] = None
    emergency_shutdown: Optional[bool] = None

class PropulsionSystem(PropulsionSystemBase):
    id: int
    spacecraft_id: int

    class Config:
        from_attributes: True





    