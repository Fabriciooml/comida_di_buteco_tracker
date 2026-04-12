from models import Bar
from scraper import parse_bar_links_and_next, parse_bar_detail


def test_parse_listing_extracts_detail_urls(fixture_html):
    html = fixture_html("listing.html")
    links, _ = parse_bar_links_and_next(html)
    assert len(links) == 2
    assert links[0] == "https://comidadibuteco.com.br/butecos/bar-exemplo-1/"
    assert links[1] == "https://comidadibuteco.com.br/butecos/bar-exemplo-2/"


def test_parse_listing_extracts_next_page(fixture_html):
    html = fixture_html("listing.html")
    _, next_url = parse_bar_links_and_next(html)
    assert next_url == "https://comidadibuteco.com.br/butecos/belo-horizonte/page/2/"


def test_parse_listing_next_page_none_on_last_page(fixture_html):
    html = fixture_html("listing_last_page.html")
    _, next_url = parse_bar_links_and_next(html)
    assert next_url is None


def test_parse_detail_extracts_all_fields(fixture_html):
    html = fixture_html("detail.html")
    url = "https://comidadibuteco.com.br/butecos/bar-exemplo-1/"
    bar = parse_bar_detail(html, url)
    assert bar.name == "Bar Exemplo 1"
    assert bar.address == "Rua das Flores, 123 | Savassi, Belo Horizonte – MG"
    assert bar.street == "Rua das Flores"
    assert bar.street_number == "123"
    assert bar.complement is None
    assert bar.neighborhood == "Savassi"
    assert bar.city == "Belo Horizonte"
    assert bar.state == "MG"
    assert bar.food_name == "Bolinho Crocante"
    assert bar.food_image_url == "https://comidadibuteco.com.br/wp-content/uploads/img.jpg"
    assert "crocante" in bar.food_description.lower()
    assert bar.working_hours == "Ter–Dom: 12h às 23h"
    assert bar.detail_url == url


def test_parse_detail_handles_missing_optional_fields():
    html = """<html><body><h1 class="section-title">Só Nome</h1></body></html>"""
    bar = parse_bar_detail(html, "https://comidadibuteco.com.br/butecos/so-nome/")
    assert isinstance(bar, Bar)
    assert bar.name == "Só Nome"
    assert bar.address is None
    assert bar.food_name is None
    assert bar.food_image_url is None
    assert bar.working_hours is None
