from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.mission import Mission as MissionModel
from app.schemas.mission import MissionCreate, Mission, MissionUpdate
from app.schemas.common import OperationStatus

router = APIRouter(prefix="/missions", tags=["Missions"])

@router.post("/", response_model=Mission, status_code=status.HTTP_201_CREATED)
def create_mission(mission: MissionCreate, db: Session = Depends(get_db)):
    try:
        db_mission = MissionModel(**mission.model_dump())
        db.add(db_mission)
        db.commit()
        db.refresh(db_mission)
        return db_mission
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not create mission: {exc}")

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
        for key, value in updated_mission.model_dump(exclude_unset=True).items():
            setattr(mission, key, value)
        db.commit()
        db.refresh(mission)
        return mission
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not update mission: {exc}")

@router.delete("/{mission_id}", response_model=OperationStatus)
def delete_mission(mission_id: int, db: Session = Depends(get_db)):
    mission = db.query(MissionModel).filter(MissionModel.id == mission_id).first()
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    try:
        db.delete(mission)
        db.commit()
        return OperationStatus(detail="Mission deleted successfully")
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not delete mission: {exc}")
