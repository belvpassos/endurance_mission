import enum
from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from app.database import Base

class NavigationStatus(enum.Enum):
    OPERATIONAL = "operational"
    STANDBY = "standby"
    ERROR = "error"
    


class NavigationSystem(Base):
    __tablename__ = "navigation_system"
    
    id = Column(Integer, primary_key=True, index=True)
    trajectory = Column(String)
    course_correction = Column(Integer)
    navigation_system_status = Column(Enum(NavigationStatus), nullable=False)
    
    spacecraft_id = Column(Integer, ForeignKey("spacecraft.id"))