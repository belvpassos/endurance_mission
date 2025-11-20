from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ResourceUsageLogBase(BaseModel):
    resource_type: str
    amount_used: float
    amount_remaining: float
    timestamp: Optional[datetime] = None  # gerado automaticamente


class ResourceUsageLogCreate(ResourceUsageLogBase):
    spacecraft_id: int


class ResourceUsageLogUpdate(BaseModel):
    resource_type: Optional[str] = None
    amount_used: Optional[float] = None
    amount_remaining: Optional[float] = None
    timestamp: Optional[datetime] = None


class ResourceUsageLog(ResourceUsageLogBase):
    id: int
    spacecraft_id: int

    class Config:
        from_attributes = True
