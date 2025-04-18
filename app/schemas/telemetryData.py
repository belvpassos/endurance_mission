from pydantic import BaseModel
from datetime import datetime

class TelemetryDataBase(BaseModel):
    timestamp: datetime
    position_x: float
    position_y: float
    position_z: float
    velocity: float
    acceleration: float
    distance_from_earth: float
    distance_to_target: float
    orbital_status: str
    pitch: float
    yaw: float
    roll: float
    mission_id: int
    
class TelemetryDataCreate(TelemetryDataBase):
    pass

class TelemetryDataResponse(TelemetryDataBase):
    id: int
    
    class Config:
        orm_mode = True