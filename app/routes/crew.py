from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import  SessionLocal
from app.models.crew import Crew as CrewModel
from app.schemas.crew import CrewCreate, CrewUpdate, Crew

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
    db.commit()
    db.refresh(db_crew)
    return db_crew

@router.get("/crew/", response_model=list[Crew])
def read_crew(db: Session = Depends(get_db)):
    return db.query(CrewModel).all()

@router.put("/crew/{crew_id}", response_model=Crew)
def update_crew_member(crew_id: int, updated_crew: CrewUpdate, db: Session = Depends(get_db)):
    crew = db.query(CrewModel).filter(CrewModel.id == crew_id).first()
    if crew is None:
        raise HTTPException(status_code=404, detail="Crew member not found")
    for key, value in updated_crew.dict(exclude_unset=True).items():
        setattr(crew, key, value)
        
    db.commit()
    db.refresh(crew)
    return crew

@router.delete("/crew/{crew_id}")
def delete_crew_member(crew_id: int, db: Session = Depends(get_db)):
    crew = db.query(CrewModel).filter(CrewModel.id == crew_id).first()
    if crew is None:
        raise HTTPException(status_code=404, detail="Crew member not found")
    
    db.delete(crew)
    db.commit()
    return{"detail":    "Crew member deleted!"}