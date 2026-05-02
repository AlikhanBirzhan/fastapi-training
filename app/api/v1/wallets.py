from fastapi import APIRouter

from app.schemas import CreateWalletRequest
from app.service import wallets as wallets_service

router = APIRouter()

@router.get('/balance')
def get_balance(wallet_name: str | None = None):
    return wallets_service.get_balance(wallet_name)

@router.post('/wallets')
def create_wallet(wallet: CreateWalletRequest):
    return wallets_service.create_wallet(wallet)