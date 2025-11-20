from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class DockingStatus(str, Enum):
    UNDOCKED = "undocked"
    DOCKING = "docking"
    DOCKED = "docked"
    FAILED = "failed"
    
class DockingSystemBase(BaseModel):
    target_module: Optional[str] = None
    status: Optional[DockingStatus] = DockingStatus.UNDOCKED
    initiated_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    success: Optional[bool] = False
    error_message: Optional[str] = None
    spacecraft_id: int   # corrigido para int
    
class DockingSystemCreate(DockingSystemBase):
    pass

class DockingSystemUpdate(BaseModel):
    target_module: Optional[str] = None
    status: Optional[DockingStatus] = None
    initiated_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    success: Optional[bool] = None
    error_message: Optional[str] = None
    spacecraft_id: Optional[int] = None
    
class DockingSystem(DockingSystemBase):
    id: int
    
    class Config:
        orm_mode = True
