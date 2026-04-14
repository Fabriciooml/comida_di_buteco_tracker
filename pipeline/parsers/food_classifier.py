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
    "carne", "boi", "vaca",
    # beef cuts
    "bife", "bifão", "bifao", "costela", "costelinha", "fraldinha", "picanha",
    "alcatra", "maminha", "ossobuco", "músculo", "musculo", "maçã de peito",
    "rabada", "mocotó", "mocoto", "tutano", "carne seca", "charque",
    # pork
    "porco", "suíno", "suino", "suína", "suina", "leitão", "leitao", "lombo", "copa lombo",
    "torresmo", "costelinha", "pernil", "pancetta", "bacon",
    "linguiça", "linguica", "chouriço", "chourico", "calabresa", "salsicha",
    "presunto", "pele suína", "pele suina", "dobradinha", "bucho",
    # poultry
    "frango", "galinha", "sobrecoxa", "coxa", "frango assado", "peru",
    "pato", "codorna",
    # offal
    "miúdo", "miudo", "fígado", "figado", "coração", "coracao",
    "moela", "moelinha", "língua", "lingua bovina", "tripa",
    # fish & seafood
    "peixe", "atum", "salmão", "salmao", "bacalhau", "tilápia", "tilapia",
    "traíra", "traira", "robalo", "pintado", "tambaqui", "surubim", "pirarucu",
    "camarão", "camarao", "frutos do mar", "lula", "polvo", "mariscos",
    "ostra", "caranguejo", "lagosta", "sardinha",
    # prepared meats
    "kafta", "almôndega", "almondega", "ragu", "pastrami",
]

_NON_VEGAN = [
    "queijo", "leite", "manteiga", "creme de leite", "nata", "iogurte",
    "requeijão", "requeijao", "ovo", "ovos", "mel", "ghee", "ricota",
    "parmesão", "parmesao", "mussarela", "mozzarela",
]


class FoodClassification(TypedDict):
    category: str | None
    is_vegan: bool
    is_vegetarian: bool


def classify_food(
    food_name: str | None,
    food_description: str | None,
) -> FoodClassification:
    if not food_name and not food_description:
        return {"category": None, "is_vegan": False, "is_vegetarian": False}

    text = " ".join(filter(None, [food_name, food_description])).lower()

    name_text = (food_name or "").lower()
    category = _detect_category(name_text) or _detect_category(text) or "pratos comuns"
    is_vegetarian = not any(kw in text for kw in _NON_VEGETARIAN)
    is_vegan = is_vegetarian and not any(kw in text for kw in _NON_VEGAN)

    return {"category": category, "is_vegan": is_vegan, "is_vegetarian": is_vegetarian}


def _detect_category(text: str) -> str | None:
    for category, keywords in _CATEGORY_KEYWORDS:
        if any(kw in text for kw in keywords):
            return category
    return None
