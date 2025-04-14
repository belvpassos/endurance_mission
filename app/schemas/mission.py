from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MissionBase(BaseModel):
    name:str
    status:str
    start_time:datetime

class MissionUpdate(BaseModel):
    name: Optional[str] = None
    launch_date: Optional[datetime] = None
    destination: Optional[str] = None
    status: Optional[str] = None

class MissionCreate(MissionBase):
    pass

class Mission(MissionBase):
    id:int
    
    class config:
        orm_mode = True
