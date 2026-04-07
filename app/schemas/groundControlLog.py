from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class GroundControlLogBase(BaseModel):
    sender: str
    receiver: str
    message_type: str
    content: str
    acknowledged: bool
    spacecraft_id: int

class GroundControlLogCreate(GroundControlLogBase):
    pass


class GroundControlLogUpdate(BaseModel):
    sender: Optional[str] = None
    receiver: Optional[str] = None
    message_type: Optional[str] = None
    content: Optional[str] = None
    acknowledged: Optional[bool] = None
    spacecraft_id: Optional[int] = None

class GroundControlLogOut(GroundControlLogBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True
