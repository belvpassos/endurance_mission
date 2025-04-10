from pydantic import BaseModel

class CrewBase(BaseModel):
    name: str
    role: str
    mission_id: int
    
class CrewCreate(CrewBase):
    pass

class Crew(CrewBase):
    id: int
    
    class config:
        orm_mode = True