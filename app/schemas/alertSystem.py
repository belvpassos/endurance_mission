from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum

class AlertType(str, Enum):
    CRITICAL = "critical"
    WARNING = "warning"
    INFO = "info"
    
class AlertBase(BaseModel):
    system: str
    alert_type: AlertType
    message: str
    acknowledged: Optional[bool] = False
    resolved: Optional[bool] = False
    resolved_at: Optional[datetime] = None
    spacecraft_id: int
    
class AlertCreate(AlertBase):
    pass

class AlertUpdate(BaseModel):
    system: Optional[str]
    alert_type: Optional[AlertType]
    message: Optional[str]
    acknowledged: Optional[bool]
    resolved: Optional[bool]
    resolved_at: Optional[datetime]
    spacecraft_id: Optional[int]
    
class Alert(AlertBase):
    id: int
    timestamp: datetime
    
    class Config:
        orm_mode = True
    