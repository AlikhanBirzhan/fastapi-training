from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.v1.users import get_current_user
from app.dependency import get_db
from app.models import User
from app.schemas import CreateWalletRequest, WalletResponse
from app.service import wallets as wallets_service

router = APIRouter()

@router.get('/balance')
def get_wallet(wallet_name: str | None = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return wallets_service.get_wallet(db, current_user, wallet_name)

@router.post('/wallets', response_model=WalletResponse)
def create_wallet(wallet: CreateWalletRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return wallets_service.create_wallet(db, current_user, wallet)