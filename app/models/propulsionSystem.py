from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from app.database import Base

class PropulsionSystem(Base):
    __tablename__ = "propulsion_system"
    
    id = Column(Integer, primary_key=True, index=True)
    thrust_level = Column(Float, nullable=False)              # força de empuxo atual
    fuel_flow_rate = Column(Float, nullable=False)            # taxa de fluxo de combustível
    engine_status = Column(String, nullable=False)            # estado atual do motor (ex: 'active', 'idle', 'error')
    active_engine = Column(String, nullable=True)             # motor ativo atual (pode ser nulo)
    emergency_shutdown = Column(Boolean, default=False)       # estado de desligamento de emergência
    
    spacecraft_id = Column(Integer, ForeignKey("spacecraft.id"), nullable=False)
