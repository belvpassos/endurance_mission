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
    system: Optional[str] = None
    alert_type: Optional[AlertType] = None
    message: Optional[str] = None
    acknowledged: Optional[bool] = None
    resolved: Optional[bool] = None
    resolved_at: Optional[datetime] = None
    spacecraft_id: Optional[int] = None

class Alert(AlertBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True
