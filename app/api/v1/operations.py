from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependency import get_db
from app.schemas import OperationRequest
from app.service import operations as operations_service

router = APIRouter()

@router.post('/operations/income')
def add_income(operation: OperationRequest, db: Session = Depends(get_db)):
    return operations_service.add_income(db, operation)

@router.post('/operations/expense')
def add_expense(operation: OperationRequest, db: Session = Depends(get_db)):
    return operations_service.add_expense(db, operation)