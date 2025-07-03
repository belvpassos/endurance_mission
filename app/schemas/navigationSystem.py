from pydantic import BaseModel #classe base do Pydantic
from enum import Enum #reaproveita o status de navegação do model
from typing import Optional #campos não obrigatórios

class NavigationStatus(str, Enum): #Enum replicado para validação no schema
    OPERATIONAL = "operational"
    STANDBY = "standby"
    ERRO9R = "error"
    
class NavigationSystemBase(BaseModel): #base do schema para create, update e response
    trajectory = str
    course_correction = str
    navigation_system_status = NavigationStatus
    
class NavigationSystemCreate(NavigationSystemBase): #Schema para criação
    spacecraft_id = int
    
class NavigationSystem(NavigationSystemBase):
    id: int
    spacecraft_id: int
    
    class Config:
        from_attributes = True

class NavigationSystemUpdate(BaseModel):
    trajectory: Optional[str] = None
    course_correction: Optional[int] = None
    navigation_system_status: Optional[str] = None 
