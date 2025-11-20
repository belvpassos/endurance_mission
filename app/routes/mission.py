from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.mission import Mission as MissionModel
from app.schemas.mission import MissionCreate, Mission, MissionUpdate

router = APIRouter(prefix="/missions", tags=["Missions"])

@router.post("/", response_model=Mission)
def create_mission(mission: MissionCreate, db: Session = Depends(get_db)):
    try:
        db_mission = MissionModel(**mission.dict())
        db.add(db_mission)
        db.commit()
        db.refresh(db_mission)
        return db_mission
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=list[Mission])
def read_missions(db: Session = Depends(get_db)):
    return db.query(MissionModel).all()

@router.get("/{mission_id}", response_model=Mission)
def read_mission(mission_id: int, db: Session = Depends(get_db)):
    mission = db.query(MissionModel).filter(MissionModel.id == mission_id).first()
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    return mission

@router.put("/{mission_id}", response_model=Mission)
def update_mission(mission_id: int, updated_mission: MissionUpdate, db: Session = Depends(get_db)):
    mission = db.query(MissionModel).filter(MissionModel.id == mission_id).first()
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    try:
        for key, value in updated_mission.dict(exclude_unset=True).items():
            setattr(mission, key, value)
        db.commit()
        db.refresh(mission)
        return mission
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{mission_id}")
def delete_mission(mission_id: int, db: Session = Depends(get_db)):
    mission = db.query(MissionModel).filter(MissionModel.id == mission_id).first()
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    try:
        db.delete(mission)
        db.commit()
        return {"detail": "Mission deleted!"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
