from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import resourceManagement as models
from app.schemas import resourceManagement as schemas
from app.schemas.common import OperationStatus

router = APIRouter(prefix="/resource-management", tags=["Resource Management"])


@router.post("/", response_model=schemas.ResourceManagement, status_code=status.HTTP_201_CREATED)
def create_resource(entry: schemas.ResourceManagementCreate, db: Session = Depends(get_db)):
    """Cria um novo registro de gerenciamento de recursos."""
    try:
        new_entry = models.ResourceManagement(**entry.model_dump())
        db.add(new_entry)
        db.commit()
        db.refresh(new_entry)
        return new_entry
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not create resource management entry: {exc}")


@router.get("/{entry_id}", response_model=schemas.ResourceManagement)
def read_resource(entry_id: int, db: Session = Depends(get_db)):
    """Retorna um registro específico de gerenciamento de recursos pelo ID."""
    entry = db.query(models.ResourceManagement).filter(models.ResourceManagement.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Resource entry not found")
    return entry


@router.get("/", response_model=list[schemas.ResourceManagement])
def read_all_resource(db: Session = Depends(get_db)):
    """Retorna todos os registros de gerenciamento de recursos."""
    return db.query(models.ResourceManagement).all()


@router.put("/{entry_id}", response_model=schemas.ResourceManagement)
def update_resource(entry_id: int, updated: schemas.ResourceManagementUpdate, db: Session = Depends(get_db)):
    """Atualiza os dados de gerenciamento de recursos de um registro específico."""
    entry = db.query(models.ResourceManagement).filter(models.ResourceManagement.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Resource entry not found")

    for key, value in updated.model_dump(exclude_unset=True).items():
        setattr(entry, key, value)

    try:
        db.commit()
        db.refresh(entry)
        return entry
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not update resource management entry: {exc}")


@router.delete("/{entry_id}", response_model=OperationStatus)
def delete_resource(entry_id: int, db: Session = Depends(get_db)):
    """Deleta um registro de gerenciamento de recursos."""
    entry = db.query(models.ResourceManagement).filter(models.ResourceManagement.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Resource entry not found")

    try:
        db.delete(entry)
        db.commit()
        return OperationStatus(detail="Resource management entry deleted successfully")
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not delete resource management entry: {exc}")
