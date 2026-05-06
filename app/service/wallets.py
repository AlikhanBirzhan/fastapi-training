from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import User
from app.schemas import CreateWalletRequest
from app.repository import wallets as wallets_repository

def get_wallet(db: Session, current_user: User, wallet_name: str | None = None):
    if wallet_name is None:
        wallets = wallets_repository.get_all_wallets(db, User.id)
        return {'total_balance': sum(w.balance for w in wallets)}
        
    if not wallets_repository.is_wallet_exist(db, current_user.id, wallet_name):
        raise HTTPException(status_code = 404, detail = f'Wallet {wallet_name} not found')
        
    wallet = wallets_repository.get_wallet_balance_by_name(db, current_user.id, wallet_name)
    return {'wallet': wallet.name, 'balance': wallet.balance}

def create_wallet(db: Session, current_user: User, wallet: CreateWalletRequest):
    if wallets_repository.is_wallet_exist(db, current_user.id, wallet.name):
        raise HTTPException(status_code=400, detail=f"Wallet '{wallet.name}' already exists")
        
    wallet = wallets_repository.create_wallet(db, current_user.id, wallet.name, wallet.initial_balance)
    db.commit()

    return {
        'message': f"Wallet '{wallet.name}' created",
        'wallet': wallet.name,
        'balance': wallet.balance
    }