# app/schemas/softwareUpdateLog.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SoftwareUpdateLogBase(BaseModel):
    version: str
    update_type: str
    status: str
    initiated_by: Optional[str] = None
    started_at: datetime
    completed_at: Optional[datetime] = None

class SoftwareUpdateLogCreate(SoftwareUpdateLogBase):
    spacecraft_id: int

class SoftwareUpdateLogUpdate(BaseModel):
    version: Optional[str] = None
    update_type: Optional[str] = None
    status: Optional[str] = None
    initiated_by: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

class SoftwareUpdateLog(SoftwareUpdateLogBase):
    id: int
    spacecraft_id: int

    class Config:
        from_attributes = True
