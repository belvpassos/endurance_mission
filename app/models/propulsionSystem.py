from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from app.database import Base

class PropulsionSystem(Base):
    __tablename__ = "propulsion_system"
    
    id = Column(Integer, primary_key=True, index=True)
    thrust_level = Column(Float)
    fuel_flow_rate = Column(Float)
    engine_status = Column(String)
    active_engine = Column(String)
    emergency_shutdown = Column(Boolean, default=False)
    
    spacecraft_id = Column(Integer, ForeignKey("spacecraft.id"))