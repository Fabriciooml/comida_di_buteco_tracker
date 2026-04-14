"""Keyword-based food attribute classifier."""
from typing import TypedDict

CATEGORIES = ["bolinhos", "torresmo e suínos", "caldos", "fritos", "assados", "pratos comuns"]

# Keywords per category, checked in order (most specific first)
_CATEGORY_KEYWORDS: list[tuple[str, list[str]]] = [
    ("torresmo e suínos", ["torresmo", "suíno", "suino", "porco", "leitão", "leitao",
                           "linguiça", "linguica", "chouriço", "chourico", "costelinha",
                           "pernil", "bacon"]),
    ("caldos",            ["caldo", "sopa", "canja", "creme de"]),
    ("bolinhos",          ["bolinho", "bolinhos", "croquete", "coxinha", "risole",
                           "risolis", "bolão", "bolao"]),
    ("fritos",            ["frito", "fritura", "pastel", "empanado", "empanada",
                           "à milanesa", "a milanesa"]),
    ("assados",           ["assado", "assada", "grelhado", "grelhada", "na brasa",
                           "no bafo", "defumado", "defumada"]),
]

_NON_VEGETARIAN = [
    # generic
    "carne", "boi", "vaca", "bovina", "bovino",
    # beef cuts
    "bife", "bifão", "bifao", "costela", "costelinha", "fraldinha", "picanha",
    "alcatra", "maminha", "ossobuco", "músculo", "musculo", "maçã de peito",
    "rabada", "mocotó", "mocoto", "tutano", "carne seca", "charque",
    "cupim", "lagarto", "contrafilé", "contrafile", "filé-mignon", "file-mignon",
    "filé mignon", "file mignon", "mignon", "mingnon", "acém", "acem", "chambaril",
    "entrecôte", "entrecote", "ponta de agulha", "ponta de peito",
    # pork
    "porco", "suíno", "suino", "suína", "suina", "leitão", "leitao", "lombo", "copa lombo",
    "torresmo", "costelinha", "pernil", "pancetta", "panceta", "bacon",
    "linguiça", "linguica", "chouriço", "chourico", "calabresa", "salsicha",
    "presunto", "pele suína", "pele suina", "dobradinha", "bucho",
    "joelho", "fumeiro", "guanciale", "salame",
    # lamb / goat / veal
    "cordeiro", "carneiro", "cabrito", "vitela",
    # rabbit / game
    "coelho", "javali",
    # poultry
    "frango", "galinha", "galeto", "sobrecoxa", "coxa", "frango assado", "peru",
    "pato", "codorna", "tulipa",
    "sassami", "drumet", "drumete", "coxinha da asa", "asa de frango",
    # offal
    "miúdo", "miudo", "fígado", "figado", "coração", "coracao",
    "moela", "moelinha", "língua", "lingua bovina", "tripa",
    # fish & seafood
    "peixe", "pescado", "atum", "salmão", "salmao", "bacalhau", "tilápia", "tilapia",
    "traíra", "traira", "robalo", "pintado", "tambaqui", "surubim", "pirarucu",
    "filhote", "badejo", "enguia", "arraia", "beijupirá", "beijupira",
    "anchova", "anchovas",
    "camarão", "camarao", "camarões", "camaroes", "frutos do mar", "lula", "polvo",
    "mariscos", "marisco", "ostra", "caranguejo", "lagosta", "sardinha",
    "siri", "mexilhão", "mexilhao", "sururu",
    # prepared meats
    "kafta", "almôndega", "almondega", "ragu", "pastrami", "pastrame",
    "polpeta", "polpetas", "hambúrguer", "hamburguer", "pulled pork",
    "alheira", "parrilla", "parilla",
    # traditional dishes (contain meat by convention)
    "feijoada", "feijão tropeiro", "feijao tropeiro", "feijão-tropeiro", "feijao-tropeiro",
    "arroz carreteiro",
]

_NON_VEGAN = [
    "queijo", "leite", "manteiga", "creme de leite", "nata", "iogurte",
    "requeijão", "requeijao", "ovo", "ovos", "mel", "ghee", "ricota",
    "parmesão", "parmesao", "mussarela", "muçarela", "mozzarela",
    "catupiry", "cajupiry", "cream cheese", "cheddar", "gema", "maionese",
]


class FoodClassification(TypedDict):
    category: str | None
    is_vegan: bool
    is_vegetarian: bool


_MIN_DESCRIPTION_WORDS = 4


def classify_food(
    food_name: str | None,
    food_description: str | None,
) -> FoodClassification:
    if not food_name and not food_description:
        return {"category": None, "is_vegan": False, "is_vegetarian": False}

    text = " ".join(filter(None, [food_name, food_description])).lower()

    name_text = (food_name or "").lower()
    category = _detect_category(name_text) or _detect_category(text) or "pratos comuns"

    desc_words = len((food_description or "").split())
    if desc_words < _MIN_DESCRIPTION_WORDS:
        return {"category": category, "is_vegan": False, "is_vegetarian": False}

    is_vegetarian = not any(kw in text for kw in _NON_VEGETARIAN)
    is_vegan = is_vegetarian and not any(kw in text for kw in _NON_VEGAN)

    return {"category": category, "is_vegan": is_vegan, "is_vegetarian": is_vegetarian}


def _detect_category(text: str) -> str | None:
    for category, keywords in _CATEGORY_KEYWORDS:
        if any(kw in text for kw in keywords):
            return category
    return None
