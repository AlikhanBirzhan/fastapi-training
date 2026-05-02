#
from fastapi import HTTPException

from app.schemas import CreateWalletRequest
from app.repository import wallets as wallets_repository

def get_balance(wallet_name: str | None = None):
    if wallet_name is None:
        wallets = wallets_repository.get_all_wallets()
        return {'total_balance': sum(wallets.values())}
    
    if not wallets_repository.is_wallet_exist(wallet_name):
        raise HTTPException(status_code = 404, detail = f'Wallet {wallet_name} not found')
    
    balance = wallets_repository.get_wallet_balance_by_name(wallet_name)
    return {'wallet': wallet_name, 'balance': balance}

def create_wallet(wallet: CreateWalletRequest):
    if wallets_repository.is_wallet_exist(wallet.name):
        raise HTTPException(status_code=400, detail=f"Wallet '{wallet.name}' already exists")
    
    new_balance = wallets_repository.create_wallet(wallet.name, wallet.initial_balance)

    return {
        'message': f"Wallet '{wallet.name}' creaeted",
        'wallet': wallet.name,
        'balance': new_balance
    }