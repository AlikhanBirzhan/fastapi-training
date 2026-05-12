from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field, field_validator
from app.enum import CurrencyEnum

# --- Auth схемы ---
class UserRegisterRequest(BaseModel):
    login: str = Field(..., max_length=127)
    password: str = Field(..., min_length=6, max_length=255)

class UserLoginRequest(BaseModel):
    login: str = Field(..., max_length=127)
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

# --- User схемы ---
class UserRequest(BaseModel):
    login: str = Field(..., max_length=127)

class UserResponse(BaseModel):
    model_config = {'from_attributes': True}
    id: int
    login: str

# --- Wallet схемы ---
class CreateWalletRequest(BaseModel):
    name: str = Field(..., max_length=127)
    initial_balance: Decimal = 0
    currency: CurrencyEnum = CurrencyEnum.KZT

    @field_validator('initial_balance')
    def balance_not_negative(cls, v: Decimal) -> Decimal:
        if v < 0:
            raise ValueError("Initial balance cannot be negative")
        return v

    @field_validator("name")
    def name_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError('Wallet name cannot be empty')
        return v

class WalletResponse(BaseModel):
    model_config = {'from_attributes': True}
    id: int
    name: str
    balance: Decimal
    currency: CurrencyEnum

# --- Operation схемы ---
class OperationRequest(BaseModel):
    wallet_name: str = Field(..., max_length=127)
    amount: Decimal
    description: str | None = Field(None, max_length=255)

    @field_validator('amount')
    def amount_must_be_positive(cls, v: Decimal) -> Decimal:
        if v <= 0:
            raise ValueError("Amount must be positive")
        return v

    @field_validator("wallet_name")
    def wallet_name_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError('Wallet name cannot be empty')
        return v

class OperationResponse(BaseModel):
    model_config = {'from_attributes': True}
    id: int
    wallet_id: int
    type: str
    amount: Decimal
    currency: CurrencyEnum
    category: str | None
    subcategory: str | None
    created_at: datetime

class PaginatedOperationsResponse(BaseModel):
    items: list[OperationResponse]
    total: int
    page: int
    limit: int
    pages: int

class TransferCreateSchema(BaseModel):
    from_wallet_id: int
    to_wallet_id: int
    amount: Decimal

    @field_validator("to_wallet_id")
    @classmethod
    def wallets_must_differ(cls, v: int, info) -> int:
        if 'from_wallet_id' in info.data and v == info.data['from_wallet_id']:
            raise ValueError("Same wallets ids!")
        return v

    @field_validator("amount")
    @classmethod
    def amount_gt_zero(cls, v: Decimal) -> Decimal:
        if v < 0:
            raise ValueError('Amount cannot be negative')
        return v

class TotalBalance(BaseModel):
    total_balance: Decimal