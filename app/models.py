from decimal import Decimal
from datetime import datetime, timezone

from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from app.enum import CurrencyEnum


class User(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]


class Wallet(Base):
    __tablename__ = 'wallet'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    balance: Mapped[Decimal] = mapped_column(Numeric(precision=18, scale=2))
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    currency: Mapped[CurrencyEnum]


class Operation(Base):
    __tablename__ = 'operation'
    id: Mapped[int] = mapped_column(primary_key=True)
    wallet_id: Mapped[int] = mapped_column(ForeignKey("wallet.id"))
    type: Mapped[str]
    amount: Mapped[Decimal] = mapped_column(Numeric(precision=18, scale=2))
    currency: Mapped[CurrencyEnum]
    category: Mapped[str | None] = mapped_column(default=None)
    subcategory: Mapped[str | None] = mapped_column(default=None)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))