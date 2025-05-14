from pydantic import BaseModel
from typing import Optional
from enum import Enum

class PriorityLevel(str, Enum):
    LOW ="low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class AnomalyDetectionBase(BaseModel):
    anomaly_logs: str
    system_alerts: str
    priority_level: PriorityLevel
  
class AnomalyDetectionCreate(AnomalyDetectionBase):
    spacecraft_id: int
    
class AnomalyDetectionUpdate(BaseModel):
    anomaly_logs: Optional[str] = None
    system_alerts: Optional[str] = None
    priority_level: Optional[PriorityLevel] = None
    spacecraft_id: Optional[int] = None
    
class AnomalyDetection(AnomalyDetectionBase):
    id: int
    spacecraft_id: int
    
class Config:
    orm_mode = True