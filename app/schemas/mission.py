from pydantic import BaseModel
from datetime import datetime

class MissionBase(BaseModel):
    name:str
    status:str
    start_time:datetime

class MissionCreate(MissionBase):
    pass

class Mission(MissionBase):
    id:int
    
    class config:
        orm_mode = True
