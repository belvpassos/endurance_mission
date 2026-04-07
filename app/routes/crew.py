from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.crew import Crew as CrewModel
from app.schemas.crew import CrewCreate, CrewUpdate, Crew
from app.schemas.common import OperationStatus

router = APIRouter(prefix="/crew", tags=["Crew"])

@router.post("/", response_model=Crew, status_code=status.HTTP_201_CREATED)
def create_crew_member(crew: CrewCreate, db: Session = Depends(get_db)):
    db_crew = CrewModel(**crew.model_dump())
    db.add(db_crew)
    try:
        db.commit()
        db.refresh(db_crew)
        return db_crew
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not create crew member: {exc}")

@router.get("/", response_model=list[Crew])
def read_crew(db: Session = Depends(get_db)):
    return db.query(CrewModel).all()

@router.get("/{crew_id}", response_model=Crew)
def read_crew_member(crew_id: int, db: Session = Depends(get_db)):
    crew = db.query(CrewModel).filter(CrewModel.id == crew_id).first()
    if not crew:
        raise HTTPException(status_code=404, detail="Crew member not found")
    return crew

@router.put("/{crew_id}", response_model=Crew)
def update_crew_member(crew_id: int, updated_crew: CrewUpdate, db: Session = Depends(get_db)):
    crew = db.query(CrewModel).filter(CrewModel.id == crew_id).first()
    if not crew:
        raise HTTPException(status_code=404, detail="Crew member not found")

    for key, value in updated_crew.model_dump(exclude_unset=True).items():
        setattr(crew, key, value)

    try:
        db.commit()
        db.refresh(crew)
        return crew
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not update crew member: {exc}")

@router.delete("/{crew_id}", response_model=OperationStatus)
def delete_crew_member(crew_id: int, db: Session = Depends(get_db)):
    crew = db.query(CrewModel).filter(CrewModel.id == crew_id).first()
    if not crew:
        raise HTTPException(status_code=404, detail="Crew member not found")

    try:
        db.delete(crew)
        db.commit()
        return OperationStatus(detail="Crew member deleted successfully")
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not delete crew member: {exc}")
