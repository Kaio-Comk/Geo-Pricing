# 🌐 Geo Pricing (geopricing)

### GeoIP-Based Localized Pricing, Currency Conversion & Purchasing Power Parity (PPP) Engine

[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg?logo=python&logoColor=white)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Dynamic localized pricing for international SaaS and subscription bots.**  
*Resolves client IP (Cloudflare safe) to ISO country code, auto-selects local payment rails, and adjusts prices to regional purchasing power parity.*

---

## 📦 Installation

```bash
pip install git+https://github.com/Kaio-Comk/Geo-Pricing.git
```

---

## 🚀 Usage

```python
from geopricing import GeoPricingEngine

engine = GeoPricingEngine(base_brl_cents=1990)
plan = engine.resolve("BR")          # country code from your own GeoIP / Cloudflare header
print(plan.currency, plan.display_price, plan.amount_cents)   # BRL R$ 19,90 1990
```

| Country | Currency | Price |
|---|---|---|
| `BR` | BRL | `base_brl_cents` (default R$ 19,90) |
| `ES`, `PT` | EUR | € 4.90 |
| `AR` | ARS | $ 4.500 |
| anything else | USD | $ 4.99 |

The country code is treated as untrusted input (it usually comes from a header): anything that is not two
letters becomes `XX` (USD) and is never echoed back. `base_brl_cents` must be a positive integer.

## 🧭 Status

What exists today is the country → currency → price table above. Not implemented yet (roadmap):

* IP → country resolution: pass the ISO code yourself (e.g. Cloudflare's `CF-IPCountry` header).
* PPP adjustment: `PPP_MULTIPLIERS` is a reference table and is not applied to prices.
* Payment rail selection, and local currencies for `MX` / `CO` (they fall back to USD).
