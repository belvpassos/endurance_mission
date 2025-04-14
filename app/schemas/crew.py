from pydantic import BaseModel
from typing import Optional

class CrewBase(BaseModel):
    name: str
    role: str
    mission_id: int
    
class CrewCreate(CrewBase):
    pass

class CrewUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    mission_id: Optional[int] = None
    
class Crew(CrewBase):
    id: int
    
    class Config:
        orm_mode = True