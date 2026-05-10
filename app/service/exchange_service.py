from decimal import Decimal
from typing import Dict, Tuple
import aiohttp
import requests

from app.enum import CurrencyEnum

FALLBACK_RATES: Dict[Tuple[str, str], Decimal] = {
    (CurrencyEnum.USD, CurrencyEnum.KZT): Decimal(str(460.95)),
    (CurrencyEnum.USD, CurrencyEnum.EUR): Decimal(str(0.85)),
    (CurrencyEnum.EUR, CurrencyEnum.KZT): Decimal(str(543.71)),
    (CurrencyEnum.EUR, CurrencyEnum.USD): Decimal(str(1.18)),
    (CurrencyEnum.KZT, CurrencyEnum.USD): Decimal(str(0.0022)),
    (CurrencyEnum.KZT, CurrencyEnum.EUR): Decimal(str(0.0018)),
}

async def get_exchange_rate(base: CurrencyEnum, target: CurrencyEnum) -> Decimal:
    url = f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/{base}.json"


    timeout = aiohttp.ClientTimeout(total=5.0)

    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url) as response:
                response.raise_for_status()
                data = await response.json()
                base_map = data.get(base, {})
                rate = base_map.get(target)

        if rate is not None and isinstance(rate, (int, float)):
            return Decimal(rate)
        raise KeyError('Rate  not found')

    except Exception:
        return FALLBACK_RATES.get((base, target), Decimal(1))
