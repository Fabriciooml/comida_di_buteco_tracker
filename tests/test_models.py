from pipeline.models import Bar


def test_bar_all_fields():
    bar = Bar(
        name="Bar do Zé",
        address="Rua das Flores, 123 — Savassi, BH",
        food_name="Bolinho de bacalhau",
        food_image_url="https://example.com/img.jpg",
        food_description="Crocante por fora, cremoso por dentro.",
        working_hours="Ter–Dom 12h–23h",
        detail_url="https://comidadibuteco.com.br/butecos/bar-do-ze/",
    )
    assert bar.name == "Bar do Zé"
    assert bar.detail_url == "https://comidadibuteco.com.br/butecos/bar-do-ze/"


def test_bar_optional_fields_default_none():
    bar = Bar(name="Mínimo", detail_url="https://comidadibuteco.com.br/butecos/minimo/")
    assert bar.address is None
    assert bar.street is None
    assert bar.street_number is None
    assert bar.complement is None
    assert bar.neighborhood is None
    assert bar.city is None
    assert bar.state is None
    assert bar.food_name is None
    assert bar.food_image_url is None
    assert bar.food_description is None
    assert bar.working_hours is None
