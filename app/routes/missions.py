from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.mission import Mission as MissionModel
from app.schemas.mission import MissionCreate, Mission

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@router.post("/missions/", response_model=Mission)
def create_mission(mission: MissionCreate, db: Session = Depends (get_db)):
    db_mission = MissionModel(**mission.dict())
    db.add(db_mission)
    db.refresh(db_mission)
    return db_mission

@router.get("/missions/", response_model=list[Mission])
def read_missions(db: Session = Depends(get_db)):
    return db.query(MissionModel).all()
