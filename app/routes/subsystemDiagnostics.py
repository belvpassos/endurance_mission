from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import subsystemDiagnostics as models
from app.schemas import subsystemDiagnostics as schemas
from app.schemas.common import OperationStatus

router = APIRouter(prefix="/subsystem-diagnostics", tags=["Subsystem Diagnostics"])

@router.post("/", response_model=schemas.SubsystemDiagnosticsResponse, status_code=status.HTTP_201_CREATED)
def create_diagnostic(entry: schemas.SubsystemDiagnosticsCreate, db: Session = Depends(get_db)):
    try:
        new_entry = models.SubsystemDiagnostics(**entry.model_dump())
        db.add(new_entry)
        db.commit()
        db.refresh(new_entry)
        return new_entry
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not create diagnostic entry: {exc}")

@router.get("/", response_model=list[schemas.SubsystemDiagnosticsResponse])
def read_all_diagnostics(db: Session = Depends(get_db)):
    return db.query(models.SubsystemDiagnostics).all()

@router.get("/{entry_id}", response_model=schemas.SubsystemDiagnosticsResponse)
def read_diagnostic(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(models.SubsystemDiagnostics).filter(models.SubsystemDiagnostics.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Diagnostic entry not found")
    return entry

@router.put("/{entry_id}", response_model=schemas.SubsystemDiagnosticsResponse)
def update_diagnostic(entry_id: int, updated: schemas.SubsystemDiagnosticsUpdate, db: Session = Depends(get_db)):
    entry = db.query(models.SubsystemDiagnostics).filter(models.SubsystemDiagnostics.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Diagnostic entry not found")
    try:
        for key, value in updated.model_dump(exclude_unset=True).items():
            setattr(entry, key, value)
        db.commit()
        db.refresh(entry)
        return entry
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not update diagnostic entry: {exc}")

@router.delete("/{entry_id}", response_model=OperationStatus)
def delete_diagnostic(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(models.SubsystemDiagnostics).filter(models.SubsystemDiagnostics.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Diagnostic entry not found")
    try:
        db.delete(entry)
        db.commit()
        return OperationStatus(detail="Diagnostic entry deleted successfully")
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not delete diagnostic entry: {exc}")
