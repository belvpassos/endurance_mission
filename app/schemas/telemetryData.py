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

class TelemetryDataUpdate(BaseModel):
    timestamp: datetime | None = None
    position_x: float | None = None
    position_y: float | None = None
    position_z: float | None = None
    velocity: float | None = None
    acceleration: float | None = None
    distance_from_earth: float | None = None
    distance_to_target: float | None = None
    orbital_status: str | None = None
    pitch: float | None = None
    yaw: float | None = None
    roll: float | None = None
    mission_id: int | None = None

class TelemetryDataResponse(TelemetryDataBase):
    id: int

    class Config:
        orm_mode = True
