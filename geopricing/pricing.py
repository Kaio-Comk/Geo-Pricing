"""
Localized pricing and currency resolution based on country and Purchasing Power Parity (PPP).
"""
from dataclasses import dataclass

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

@dataclass
class LocalizedPlan:
    country_code: str
    currency: str
    display_price: str
    amount_cents: int

class GeoPricingEngine:
    def __init__(self, base_brl_cents: int = 1990):
        self.base_brl_cents = base_brl_cents

    def resolve(self, country_code: str) -> LocalizedPlan:
        cc = country_code.upper().strip()
        currency = COUNTRY_CURRENCIES.get(cc, "USD")
        
        if currency == "BRL":
            return LocalizedPlan("BR", "BRL", "R$ 19,90", 1990)
        elif currency == "EUR":
            return LocalizedPlan(cc, "EUR", "€ 4.90", 490)
        elif currency == "ARS":
            return LocalizedPlan("AR", "ARS", "$ 4.500", 450000)
        else:
            return LocalizedPlan(cc, "USD", "$ 4.99", 499)
