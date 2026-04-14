from pipeline.parsers.food_classifier import CATEGORIES, classify_food


def test_classify_food_returns_valid_category():
    result = classify_food("Bolinho de bacalhau", "Crocante por fora, cremoso por dentro.")
    assert result["category"] == "bolinhos"
    assert result["category"] in CATEGORIES


def test_classify_torresmo():
    result = classify_food("Torresmo", "Torresmo crocante temperado.")
    assert result["category"] == "torresmo e suínos"


def test_classify_caldo():
    result = classify_food("Caldo de feijão", "Caldo encorpado com bacon e calabresa.")
    assert result["category"] == "caldos"


def test_classify_frito():
    result = classify_food("Pastel frito", "Pastel crocante frito na hora.")
    assert result["category"] == "fritos"


def test_classify_assado():
    result = classify_food("Frango assado", "Frango assado com ervas.")
    assert result["category"] == "assados"


def test_classify_prato_comum_fallback():
    result = classify_food("Prato do dia", "Prato especial da casa.")
    assert result["category"] == "pratos comuns"


def test_is_not_vegetarian_when_has_meat():
    result = classify_food("Costela", "Costela bovina assada no bafo.")
    assert result["is_vegetarian"] is False
    assert result["is_vegan"] is False


def test_is_not_vegetarian_when_has_fish():
    result = classify_food("Bolinho de bacalhau", "Recheado com bacalhau desfiado.")
    assert result["is_vegetarian"] is False
    assert result["is_vegan"] is False


def test_is_vegetarian_but_not_vegan_with_dairy():
    result = classify_food("Bolinho de queijo", "Bolinho recheado com queijo mineiro.")
    assert result["is_vegetarian"] is True
    assert result["is_vegan"] is False


def test_is_vegan_when_no_animal_ingredients():
    result = classify_food("Bolinho de mandioca", "Bolinho crocante de mandioca com temperos.")
    assert result["is_vegan"] is True
    assert result["is_vegetarian"] is True


def test_empty_inputs_returns_defaults():
    result = classify_food(None, None)
    assert result["category"] is None
    assert result["is_vegan"] is False
    assert result["is_vegetarian"] is False


# --- misclassification regression tests ---

def test_ossobuco_is_not_vegetarian():
    result = classify_food("Ossobuco", "Ossobuco com angu e couve.")
    assert result["is_vegetarian"] is False

def test_lombo_is_not_vegetarian():
    result = classify_food("Copa lombo", "Copa lombo assado com escarola e farofa de soja.")
    assert result["is_vegetarian"] is False

def test_tilapia_is_not_vegetarian():
    result = classify_food("Tilápia Roletera", "Roletes de filé de tilápia empanado com rúcula.")
    assert result["is_vegetarian"] is False

def test_moela_is_not_vegetarian():
    result = classify_food("Moela ao molho", "Moelinha ao molho acompanhada de peixinho da horta.")
    assert result["is_vegetarian"] is False

def test_almondega_is_not_vegetarian():
    result = classify_food("Almôndega", "Almôndega aberta na chapa com repolho ao vinho.")
    assert result["is_vegetarian"] is False

def test_musculo_is_not_vegetarian():
    result = classify_food("Músculo do Popeye", "Músculo com purê de batata e espinafre.")
    assert result["is_vegetarian"] is False

def test_calabresa_is_not_vegetarian():
    result = classify_food("Caldo de feijão", "Caldo encorpado com calabresa e bacon.")
    assert result["is_vegetarian"] is False

def test_pancetta_is_not_vegetarian():
    result = classify_food("Trem de Minas", "Hot de copa lombo recheado com agrião, pancetta.")
    assert result["is_vegetarian"] is False

def test_kafta_is_not_vegetarian():
    result = classify_food("Kafta", "Kafta recheada com queijo, acompanha batata e salada.")
    assert result["is_vegetarian"] is False

def test_bife_is_not_vegetarian():
    result = classify_food("Bifão", "Bifão de copa lombo com creme de espinafre.")
    assert result["is_vegetarian"] is False

def test_peru_is_not_vegetarian():
    result = classify_food("Glu Glu à Baiana", "Pescoço de peru à baiana.")
    assert result["is_vegetarian"] is False

def test_dobradinha_is_not_vegetarian():
    result = classify_food("Língua Dobrada", "Língua com dobradinha bovina e champignon.")
    assert result["is_vegetarian"] is False

def test_traira_is_not_vegetarian():
    result = classify_food("Uai, Traíra", "Traíra com purê de mandioca e crispy de couve.")
    assert result["is_vegetarian"] is False

def test_sobrecoxa_is_not_vegetarian():
    result = classify_food("Flor de Minas", "Sobrecoxa desossada e empanada com mix de verduras.")
    assert result["is_vegetarian"] is False

def test_suina_feminine_is_not_vegetarian():
    result = classify_food("Porkin do Popeye", "Croquete de barriga suína, recheada com mix de espinafre.")
    assert result["is_vegetarian"] is False
