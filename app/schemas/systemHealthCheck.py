from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SystemHealthCheckBase(BaseModel):
    spacecraft_id: int
    timestamp: datetime
    system_name: str
    status: str
    message: Optional[str] = None

class SystemHealthCheckCreate(SystemHealthCheckBase):
    pass

class SystemHealthCheckUpdate(BaseModel):
    timestamp: Optional[datetime] = None
    system_name: Optional[str] = None
    status: Optional[str] = None
    message: Optional[str] = None

class SystemHealthCheckResponse(SystemHealthCheckBase):
    id: int

    class Config:
        from_attributes = True
