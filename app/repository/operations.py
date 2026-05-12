from datetime import datetime
from decimal import Decimal
from sqlalchemy.orm import Session
from app.enum import CurrencyEnum
from app.models import Operation


def create_operation(
    db: Session,
    wallet_id: int,
    type: str,
    amount: Decimal,
    currency: CurrencyEnum,
    category: str | None = None,
    subcategory: str | None = None
) -> Operation:
    operation = Operation(
        wallet_id=wallet_id,
        type=type,
        amount=amount,
        currency=currency,
        category=category,
        subcategory=subcategory,
    )
    db.add(operation)
    db.flush()
    return operation


def get_operations_list(
    db: Session,
    wallets_ids: list[int],
    date_from: datetime | None,
    date_to: datetime | None,
    page: int,
    limit: int
) -> tuple[list[Operation], int]:
    query = db.query(Operation).filter(Operation.wallet_id.in_(wallets_ids))

    if date_from:
        query = query.filter(Operation.created_at >= date_from)
    if date_to:
        query = query.filter(Operation.created_at <= date_to)

    total = query.count()

    operations = (
        query
        .order_by(Operation.created_at.desc())
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return operations, total