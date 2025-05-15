from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CommandQueueBase(BaseModel):
    command: str
    parameters: Optional[str] = None
    schedule_time: Optional[datetime] = None
    executed: Optional [bool] = False
    executed_time: Optional[datetime] = None
    priority: Optional[int] = 1
    status: Optional[str] = "scheduled"
    spacecraft_id: int
    
class CommandQueueCreate(CommandQueueBase):
    pass

class CommandQueueUpdate(BaseModel):
    command: Optional[str] = None
    parameters: Optional[str] = None
    schedule_time: Optional[datetime] = None
    executed: Optional[bool] = None
    executed_time: Optional[datetime] = None
    priority: Optional[int] = None
    status: Optional[str] = None
    spacecraft_id: Optional[int] = None
    
class CommandQueue(CommandQueueBase):
    id:int
    
    class Config:
        orm_mode = True
    

    
    