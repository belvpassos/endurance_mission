from pydantic import BaseModel
from enum import Enum
from datetime import datetime
from typing import Optional

class PayloadSystemStatus(str, Enum):
    ACTIVE = "active"
    STANDBY = "standby"
    DEPLOYED = "deployed"
    FAILED = "failed"
    DECOMMISSIONED = "decommissioned"
    
    

class PayloadSystemBase(BaseModel):
    name: str
    type: str
    status: PayloadSystemStatus
    mass: float
    power_requirement: float
    data_rate: float
    deployment_time: datetime
    
class PayloadSystemCreate(PayloadSystemBase):
    spacecraft_id: int
    
class PayloadSystem(PayloadSystemBase):
    id: int
    spacecraft_id: int
    
    class Config:
        from_attributes = True
        
class PayloadSystemUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    status: Optional[PayloadSystemStatus] = None
    mass: Optional[float] = None
    power_requirement: Optional[float] = None
    data_rate: Optional[float] = None
    deployment_time: Optional[datetime] = None
    