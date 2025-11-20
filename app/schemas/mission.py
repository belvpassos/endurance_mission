from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MissionBase(BaseModel):
    name: str
    status: str
    start_time: Optional[datetime] = None  # deixa opcional para criar sem passar

class MissionCreate(MissionBase):
    pass

class MissionUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = None
    start_time: Optional[datetime] = None

class Mission(MissionBase):
    id: int

    class Config:
        orm_mode = True
