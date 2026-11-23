"""
Localized pricing and currency resolution based on the country code.

Prices come from a fixed table per currency. `PPP_MULTIPLIERS` is a reference table only:
Purchasing Power Parity is NOT applied to the prices (see README).
"""
import re
from dataclasses import dataclass

_ISO2 = re.compile(r"[A-Z]{2}")
UNKNOWN_COUNTRY = "XX"   # same code Cloudflare uses when it cannot tell the country

COUNTRY_CURRENCIES = {
    "BR": "BRL",
    "US": "USD",
    "ES": "EUR",
    "PT": "EUR",
    "AR": "ARS",
    "MX": "MXN",
    "CO": "COP",
}

PPP_MULTIPLIERS = {
    "BR": 1.0,
    "US": 1.0,
    "ES": 0.85,
    "AR": 0.45,
    "CO": 0.50,
}

def _format_brl(cents: int) -> str:
    """1990 -> 'R$ 19,90'; 123456 -> 'R$ 1.234,56'."""
    reais, centavos = divmod(cents, 100)
    return f"R$ {reais:,}".replace(",", ".") + f",{centavos:02d}"

@dataclass
class LocalizedPlan:
    country_code: str
    currency: str
    display_price: str
    amount_cents: int

def normalize_country(value) -> str:
    """ISO 3166-1 alpha-2 in upper case, or 'XX'. The value usually comes from a request header
    (e.g. CF-IPCountry), so anything else is untrusted input and is never echoed back."""
    cc = str(value or "").strip()
    if not cc.isascii():          # str.upper() expands some letters ("ß" -> "SS", "ﬀ" -> "FF")
        return UNKNOWN_COUNTRY
    cc = cc.upper()
    return cc if _ISO2.fullmatch(cc) else UNKNOWN_COUNTRY

class GeoPricingEngine:
    def __init__(self, base_brl_cents: int = 1990):
        if isinstance(base_brl_cents, bool) or not isinstance(base_brl_cents, int) or base_brl_cents <= 0:
            raise ValueError(f"base_brl_cents must be a positive integer, got {base_brl_cents!r}")
        self.base_brl_cents = base_brl_cents

    def resolve(self, country_code) -> LocalizedPlan:
        cc = normalize_country(country_code)
        currency = COUNTRY_CURRENCIES.get(cc, "USD")
        
        if currency == "BRL":
            cents = self.base_brl_cents
            return LocalizedPlan("BR", "BRL", _format_brl(cents), cents)
        elif currency == "EUR":
            return LocalizedPlan(cc, "EUR", "€ 4.90", 490)
        elif currency == "ARS":
            return LocalizedPlan("AR", "ARS", "$ 4.500", 450000)
        else:
            return LocalizedPlan(cc, "USD", "$ 4.99", 499)
