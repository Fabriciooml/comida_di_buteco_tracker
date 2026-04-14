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

def test_vague_description_is_not_vegetarian():
    result = classify_food("Pastel desconstruído", "Recheio à parte.")
    assert result["is_vegetarian"] is False
    assert result["is_vegan"] is False

def test_no_description_is_not_vegetarian():
    result = classify_food("Prato do dia", None)
    assert result["is_vegetarian"] is False
    assert result["is_vegan"] is False


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

def test_cupim_is_not_vegetarian():
    result = classify_food("Cupim Verde da Mamma", "Cupim assado, servido com pesto de agrião.")
    assert result["is_vegetarian"] is False

def test_lagarto_is_not_vegetarian():
    result = classify_food("O Lagarto", "Lagarto desfiado, assado e defumado no bafo.")
    assert result["is_vegetarian"] is False

def test_contrafile_is_not_vegetarian():
    result = classify_food("Contrafilé do chef", "Tiras de contrafilé acebolado na chapa com brócolis.")
    assert result["is_vegetarian"] is False

def test_file_mignon_is_not_vegetarian():
    result = classify_food("Espetinho Poró e Brasa", "Espetinho de filé-mignon com molho autoral de tomate.")
    assert result["is_vegetarian"] is False

def test_mignon_alone_is_not_vegetarian():
    result = classify_food("Mignon da Lú", "Mignon acompanhado de couve refogada e farofa.")
    assert result["is_vegetarian"] is False

def test_bovina_is_not_vegetarian():
    result = classify_food("Panelada Matuta", "Panelada bovina com cuscuz e salada fresca.")
    assert result["is_vegetarian"] is False

def test_sassami_is_not_vegetarian():
    result = classify_food("Sassami do Popeye", "Sassami empanado e frito, finalizado com muçarela.")
    assert result["is_vegetarian"] is False

def test_drumet_is_not_vegetarian():
    result = classify_food("Drumet da Villa", "Coxinha da asa recheada com queijo minas e espinafre.")
    assert result["is_vegetarian"] is False

def test_chambaril_is_not_vegetarian():
    result = classify_food("Cabuloso", "Croquete cremoso de chambaril, recheado com muçarela.")
    assert result["is_vegetarian"] is False

def test_cordeiro_is_not_vegetarian():
    result = classify_food("Quibe da Lagoa", "Quibe de cordeiro, temperado com hortelã e couve-flor.")
    assert result["is_vegetarian"] is False

def test_galeto_is_not_vegetarian():
    result = classify_food("Galetinho do Rei", "Galeto marinado no tempero especial do Rei e assado.")
    assert result["is_vegetarian"] is False

def test_siri_is_not_vegetarian():
    result = classify_food("Siri do Mato", "Bolinho recheado com siri catado e couve.")
    assert result["is_vegetarian"] is False

def test_mexilhao_is_not_vegetarian():
    result = classify_food("Mexilhoba", "Mexilhão ao molho de tomate, cebola e taioba.")
    assert result["is_vegetarian"] is False

def test_sururu_is_not_vegetarian():
    result = classify_food("Maxixada Praiana", "Ensopado de maxixe com sururu e farofa de couve.")
    assert result["is_vegetarian"] is False

def test_camaroes_plural_is_not_vegetarian():
    result = classify_food("Made in Bahia", "Casquinha de siri com camarões e couve.")
    assert result["is_vegetarian"] is False

def test_filhote_is_not_vegetarian():
    result = classify_food("Mar e terra", "Filhote assado na brasa com chutney de maracujá.")
    assert result["is_vegetarian"] is False

def test_pulled_pork_is_not_vegetarian():
    result = classify_food("Barquinhas De Endívia", "Barquinhas recheadas com pulled pork defumado.")
    assert result["is_vegetarian"] is False

def test_salame_is_not_vegetarian():
    result = classify_food("Poró & Prosa", "Pasta de tomate seco com salame, parmesão e alho-poró.")
    assert result["is_vegetarian"] is False

def test_panceta_is_not_vegetarian():
    result = classify_food("Panceta à pururuca", "Panceta à pururuca, acompanha molhos de alho-poró.")
    assert result["is_vegetarian"] is False

def test_hamburguer_is_not_vegetarian():
    result = classify_food("TCC Burger", "Minipão de hambúrguer com mini-hambúrguer e agrião.")
    assert result["is_vegetarian"] is False

def test_mucarela_is_not_vegan():
    result = classify_food("Botequiche", "Quiche de alho-poró com muçarela. Servido com molho arretado.")
    assert result["is_vegan"] is False
    assert result["is_vegetarian"] is True

def test_catupiry_is_not_vegan():
    result = classify_food("Broconzola", "Bolinho de brócolis com gorgonzola e catupiry.")
    assert result["is_vegan"] is False
    assert result["is_vegetarian"] is True

def test_cream_cheese_is_not_vegan():
    result = classify_food("Pastel de alho-poró com cream cheese", "Minipastéis recheados com alho-poró e cream cheese.")
    assert result["is_vegan"] is False
    assert result["is_vegetarian"] is True

def test_cheddar_is_not_vegan():
    result = classify_food("TCC Burger", "Minipão de hambúrguer com mini-hambúrguer, agrião e maionese com cheddar.")
    assert result["is_vegan"] is False

def test_feijoada_is_not_vegetarian():
    result = classify_food("Bolinho de feijoada", "Bolinho de feijoada com geleia de laranja com pimenta.")
    assert result["is_vegetarian"] is False

def test_feijao_tropeiro_is_not_vegetarian():
    result = classify_food("Tropeirão Safado", "Feijão-tropeiro especial com o tempero da Vó Maria.")
    assert result["is_vegetarian"] is False

def test_feijao_tropeiro_space_is_not_vegetarian():
    result = classify_food("Disco de feijão tropeiro", "Disco de feijão tropeiro com molho de pimenta.")
    assert result["is_vegetarian"] is False

def test_tulipa_is_not_vegetarian():
    result = classify_food("Tulipinha", "Porção de tulipa com molho de alho e alho-poró.")
    assert result["is_vegetarian"] is False

def test_arroz_carreteiro_is_not_vegetarian():
    result = classify_food("Arancini de carreteiro", "Bolinho de arroz carreteiro da casa.")
    assert result["is_vegetarian"] is False

def test_maionese_is_not_vegan():
    result = classify_food("Bolinho de mandioca", "Bolinho crocante de mandioca com maionese da casa.")
    assert result["is_vegan"] is False
    assert result["is_vegetarian"] is True
