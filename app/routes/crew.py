from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import  SessionLocal
from app.models.crew import Crew as CrewModel
from app.schemas.crew import CrewCreate, Crew

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@router.post("/crew/", response_model=Crew)
def create_crew_member(crew: CrewCreate, db: Session = Depends(get_db)):
    db_crew = CrewModel(**crew.dict())
    db.add(db_crew)
    db.comit()
    db.refresh(db_crew)
    return db_crew

@router.get("/crew/", response_model=list[Crew])
def read_crew(db: Session = Depends(get_db)):
    return db.query(CrewModel).all()