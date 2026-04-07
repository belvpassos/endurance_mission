from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.abortRecoverySystem import AbortRecoverySystem
from app.schemas import abortRecoverySystem as schemas
from app.schemas.common import OperationStatus

router = APIRouter(prefix="/abort-recovery", tags=["Abort Recovery System"])

# Criar entrada
@router.post("/", response_model=schemas.AbortRecovery, status_code=status.HTTP_201_CREATED)
def create_abort_recovery(entry: schemas.AbortRecoveryCreate, db: Session = Depends(get_db)):
    try:
        new_entry = AbortRecoverySystem(**entry.model_dump())
        db.add(new_entry)
        db.commit()
        db.refresh(new_entry)
        return new_entry
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not create abort recovery entry: {exc}")

# Ler uma entrada pelo ID
@router.get("/{entry_id}", response_model=schemas.AbortRecovery)
def read_abort_recovery(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(AbortRecoverySystem).filter(AbortRecoverySystem.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Abort Recovery entry not found")
    return entry

# Ler todas as entradas
@router.get("/", response_model=list[schemas.AbortRecovery])
def read_all_abort_recovery(db: Session = Depends(get_db)):
    return db.query(AbortRecoverySystem).all()

# Atualizar entrada
@router.put("/{entry_id}", response_model=schemas.AbortRecovery)
def update_abort_recovery(entry_id: int, updated: schemas.AbortRecoveryUpdate, db: Session = Depends(get_db)):
    entry = db.query(AbortRecoverySystem).filter(AbortRecoverySystem.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Abort Recovery entry not found")
    
    try:
        for key, value in updated.model_dump(exclude_unset=True).items():
            setattr(entry, key, value)
        db.commit()
        db.refresh(entry)
        return entry
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not update abort recovery entry: {exc}")

# Deletar entrada
@router.delete("/{entry_id}", response_model=OperationStatus)
def delete_abort_recovery(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(AbortRecoverySystem).filter(AbortRecoverySystem.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Abort Recovery entry not found")
    
    try:
        db.delete(entry)
        db.commit()
        return OperationStatus(detail="Abort recovery entry deleted successfully")
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not delete abort recovery entry: {exc}")
