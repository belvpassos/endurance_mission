from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class GroundControlLogBase(BaseModel):
    sender: str
    receiver: str
    message_type: str
    content: str
    acknowledged: bool
    spacecraft_id: int
    
class GroundControlLogCreate(GroundControlLogBase):
    pass

class GroundControlLogOut(GroundControlLogBase):
    id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True