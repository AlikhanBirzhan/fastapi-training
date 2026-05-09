from decimal import Decimal
from typing import Dict, Tuple

from app.enum import CurrencyEnum

FALLBACK_RATES: Dict[Tuple[str, str], Decimal] = {
    (CurrencyEnum.USD, CurrencyEnum.KZT): Decimal(str(460.95)),
    (CurrencyEnum.USD, CurrencyEnum.EUR): Decimal(str(0.85)),
    (CurrencyEnum.EUR, CurrencyEnum.KZT): Decimal(str(543.71)),
    (CurrencyEnum.EUR, CurrencyEnum.USD): Decimal(str(1.18)),
    (CurrencyEnum.KZT, CurrencyEnum.USD): Decimal(str(0.0022)),
    (CurrencyEnum.KZT, CurrencyEnum.EUR): Decimal(str(0.0018)),
}

def get_exchange_rate(base: CurrencyEnum, target: CurrencyEnum) -> Decimal:
    return FALLBACK_RATES.get((base, target), Decimal(1))