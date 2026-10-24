from geopricing import GeoPricingEngine

def test_resolve_pricing():
    engine = GeoPricingEngine(base_brl_cents=1990)
    br = engine.resolve("BR")
    assert br.currency == "BRL"
    assert br.display_price == "R$ 19,90"
    
    es = engine.resolve("ES")
    assert es.currency == "EUR"
    assert "€" in es.display_price
