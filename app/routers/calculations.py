from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.auth import compute_result
from app.database import get_db

router = APIRouter(prefix="/calculations", tags=["calculations"])


def _get_or_404(calc_id: int, db: Session) -> models.Calculation:
    calc = db.get(models.Calculation, calc_id)
    if not calc:
        raise HTTPException(status_code=404, detail="Calculation not found")
    return calc


# Browse
@router.get("/", response_model=list[schemas.CalculationRead])
def browse(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Calculation).offset(skip).limit(limit).all()


# Read
@router.get("/{calc_id}", response_model=schemas.CalculationRead)
def read(calc_id: int, db: Session = Depends(get_db)):
    return _get_or_404(calc_id, db)


# Add
@router.post("/", response_model=schemas.CalculationRead, status_code=201)
def add(payload: schemas.CalculationCreate, db: Session = Depends(get_db)):
    try:
        result = compute_result(payload.operation, payload.operand_a, payload.operand_b)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))

    # user_id=1 as placeholder; replace with auth dependency if using JWT
    calc = models.Calculation(
        operation=payload.operation,
        operand_a=payload.operand_a,
        operand_b=payload.operand_b,
        result=result,
        user_id=1,
    )
    db.add(calc)
    db.commit()
    db.refresh(calc)
    return calc


# Edit (partial update)
@router.patch("/{calc_id}", response_model=schemas.CalculationRead)
def edit(calc_id: int, payload: schemas.CalculationUpdate, db: Session = Depends(get_db)):
    calc = _get_or_404(calc_id, db)

    updated = payload.model_dump(exclude_unset=True)
    for field, value in updated.items():
        setattr(calc, field, value)

    # Recompute result with current values
    try:
        calc.result = compute_result(calc.operation, calc.operand_a, calc.operand_b)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))

    db.commit()
    db.refresh(calc)
    return calc


# Delete
@router.delete("/{calc_id}", status_code=204)
def delete(calc_id: int, db: Session = Depends(get_db)):
    calc = _get_or_404(calc_id, db)
    db.delete(calc)
    db.commit()