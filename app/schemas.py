from decimal import Decimal

from pydantic import BaseModel, Field, field_validator

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

class CreateWalletRequest(BaseModel):
    name: str = Field(..., max_length=127)
    initial_balance: Decimal = 0

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
    
class UserRequest(BaseModel):
    login: str = Field(..., max_length=127)

class UserResponse(UserRequest):
    model_config = {'from_attributes': True}

    id: int