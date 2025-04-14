from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.mission import Mission as MissionModel
from app.schemas.mission import MissionCreate, Mission, MissionUpdate

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/missions/", response_model=Mission)
def create_mission(mission: MissionCreate, db: Session = Depends(get_db)):
    db_mission = MissionModel(**mission.dict())
    db.add(db_mission)
    db.commit()
    db.refresh(db_mission)
    return db_mission

@router.get("/missions/", response_model=list[Mission])
def read_missions(db: Session = Depends(get_db)):
    return db.query(MissionModel).all()

@router.get("/missions/{mission_id}", response_model=Mission)
def read_mission(mission_id: int, db: Session = Depends(get_db)):
    mission = db.query(MissionModel).filter(MissionModel.id == mission_id).first()
    if mission is None:
        raise HTTPException(status_code=404, detail="Mission not found")
    return mission

@router.put("/missions/{mission_id}", response_model=Mission)
def update_mission(mission_id: int, updated_mission: MissionUpdate, db: Session = Depends(get_db)):
    mission = db.query(MissionModel).filter(MissionModel.id == mission_id).first()
    if mission is None:
        raise HTTPException(status_code=404, detail="Mission not found")
    
    for key, value in updated_mission.dict(exclude_unset=True).items():
        setattr(mission, key, value)

    db.commit()
    db.refresh(mission)
    return mission

@router.delete("/missions/{mission_id}")
def delete_mission(mission_id: int, db: Session = Depends(get_db)):
    mission = db.query(MissionModel).filter(MissionModel.id == mission_id).first()
    if mission is None:
        raise HTTPException(status_code=404, detail="Mission not found")
    
    db.delete(mission)
    db.commit()
    return {"detail": "Mission deleted!"}
