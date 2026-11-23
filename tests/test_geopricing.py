from geopricing import GeoPricingEngine

def test_resolve_pricing():
    engine = GeoPricingEngine(base_brl_cents=1990)
    br = engine.resolve("BR")
    assert br.currency == "BRL"
    assert br.display_price == "R$ 19,90"
    
    es = engine.resolve("ES")
    assert es.currency == "EUR"
    assert "€" in es.display_price

def test_default_brl_price_unchanged():
    br = GeoPricingEngine().resolve(" br ")
    assert (br.country_code, br.currency, br.display_price, br.amount_cents) == ("BR", "BRL", "R$ 19,90", 1990)

def test_custom_brl_base_is_used():
    br = GeoPricingEngine(base_brl_cents=123456).resolve("BR")
    assert br.amount_cents == 123456
    assert br.display_price == "R$ 1.234,56"

def test_unknown_country_falls_back_to_usd():
    plan = GeoPricingEngine().resolve("JP")
    assert (plan.country_code, plan.currency, plan.amount_cents) == ("JP", "USD", 499)

def test_codigo_de_pais_invalido_nao_e_devolvido():
    e = GeoPricingEngine()
    for ruim in ("<script>alert(1)</script>", None, "", "BRA", "B1", 42):
        plan = e.resolve(ruim)
        assert (plan.country_code, plan.currency) == ("XX", "USD"), ruim

def test_letra_nao_ascii_nao_vira_codigo_de_pais():
    # 05/11/2026: str.upper() expands "ß" -> "SS" and "ﬀ" -> "FF", which used to pass as a country code.
    from geopricing.pricing import normalize_country
    for ruim in ("ß", "ﬀ", "ＢＲ", "bŕ"):
        assert normalize_country(ruim) == "XX", ruim
    assert normalize_country(" br ") == "BR"

def test_preco_base_precisa_ser_inteiro_positivo():
    import pytest
    for ruim in (0, -5, 19.9, "1990", True):
        with pytest.raises(ValueError):
            GeoPricingEngine(base_brl_cents=ruim)
