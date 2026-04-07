from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import propulsionSystem as models
from app.schemas import propulsionSystem as schemas
from app.schemas.common import OperationStatus

router = APIRouter(prefix="/propulsion-system", tags=["Propulsion System"])


@router.post("/", response_model=schemas.PropulsionSystem, status_code=status.HTTP_201_CREATED)
def create_propulsion(entry: schemas.PropulsionSystemCreate, db: Session = Depends(get_db)):
    """Cria um novo registro de sistema de propulsão."""
    try:
        new_entry = models.PropulsionSystem(**entry.model_dump())
        db.add(new_entry)
        db.commit()
        db.refresh(new_entry)
        return new_entry
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not create propulsion entry: {exc}")


@router.get("/{entry_id}", response_model=schemas.PropulsionSystem)
def read_propulsion(entry_id: int, db: Session = Depends(get_db)):
    """Retorna um sistema de propulsão específico pelo ID."""
    entry = db.query(models.PropulsionSystem).filter(models.PropulsionSystem.id == entry_id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Propulsion entry not found")
    return entry


@router.get("/", response_model=list[schemas.PropulsionSystem])
def read_all_propulsion(db: Session = Depends(get_db)):
    """Retorna todos os sistemas de propulsão registrados."""
    return db.query(models.PropulsionSystem).all()


@router.put("/{entry_id}", response_model=schemas.PropulsionSystem)
def update_propulsion(entry_id: int, updated: schemas.PropulsionSystemUpdate, db: Session = Depends(get_db)):
    """Atualiza os parâmetros de um sistema de propulsão."""
    entry = db.query(models.PropulsionSystem).filter(models.PropulsionSystem.id == entry_id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Propulsion entry not found")

    for key, value in updated.model_dump(exclude_unset=True).items():
        setattr(entry, key, value)

    try:
        db.commit()
        db.refresh(entry)
        return entry
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not update propulsion entry: {exc}")


@router.delete("/{entry_id}", response_model=OperationStatus)
def delete_propulsion(entry_id: int, db: Session = Depends(get_db)):
    """Deleta um sistema de propulsão específico."""
    entry = db.query(models.PropulsionSystem).filter(models.PropulsionSystem.id == entry_id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Propulsion entry not found")

    try:
        db.delete(entry)
        db.commit()
        return OperationStatus(detail="Propulsion entry deleted successfully")
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not delete propulsion entry: {exc}")
