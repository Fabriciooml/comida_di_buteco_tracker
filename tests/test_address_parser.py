from address_parser import parse_address


def test_standard_address():
    r = parse_address("Rua Alberto Cintra, 47 | União, Belo Horizonte – MG")
    assert r["street"] == "Rua Alberto Cintra"
    assert r["street_number"] == "47"
    assert r["complement"] is None
    assert r["neighborhood"] == "União"
    assert r["city"] == "Belo Horizonte"
    assert r["state"] == "MG"


def test_abbreviated_street_type():
    r = parse_address("Av. Silviano Brandão, 1293 | Sagrada Família, Belo Horizonte – MG")
    assert r["street"] == "Av. Silviano Brandão"
    assert r["street_number"] == "1293"
    assert r["neighborhood"] == "Sagrada Família"


def test_address_with_letter_complement():
    r = parse_address("R. Professor Raimundo Nonato, 31 – A | Santa Tereza, Belo Horizonte – MG")
    assert r["street_number"] == "31"
    assert r["complement"] == "A"


def test_address_with_word_complement():
    r = parse_address("Av. Augusto de Lima, 233 – Varanda | Centro, Belo Horizonte – MG")
    assert r["street_number"] == "233"
    assert r["complement"] == "Varanda"


def test_none_input_returns_none_fields():
    r = parse_address(None)
    assert all(v is None for v in r.values())


def test_unrecognized_format_returns_none_fields():
    r = parse_address("Somewhere unknown")
    assert all(v is None for v in r.values())


def test_neighborhood_correction_santa_teresa():
    r = parse_address("R. Pirite, 187 | Santa Teresa, Belo Horizonte – MG")
    assert r["neighborhood"] == "Santa Tereza"


def test_neighborhood_with_parenthetical():
    r = parse_address(
        "R. Pastor Rui Franco, 257 | São João Batista (Venda Nova), Belo Horizonte – MG"
    )
    assert r["neighborhood"] == "São João Batista (Venda Nova)"
