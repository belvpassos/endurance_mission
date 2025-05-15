from pydantic import BaseModel
from typing import Optional
from enum import Enum
from datetime import datetime

class LinkStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"

class CommunicationBase(BaseModel):
    latency: Optional[float] = None
    signal_strength: Optional[float] = None
    uplink_status: LinkStatus
    downlink_status: LinkStatus
    last_contacted_time: Optional[datetime] = None
    
class CommunicationCreate(CommunicationBase):
    spacecraft_id: int
    
class CommunicationUpdate(BaseModel):
    latency: Optional[float] = None
    signal_strength: Optional[float] = None
    uplink_status: Optional[LinkStatus] = None
    downlink_status: Optional[LinkStatus] = None
    last_contact_time: Optional[datetime] = None
    
class Communication(CommunicationBase):
    id: int
    spacecraft_id: int
    
    class Config:
        orm_mode = True
