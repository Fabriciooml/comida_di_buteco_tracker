import re
from typing import AsyncGenerator
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright, Page
from pipeline.parsers.address_parser import parse_address
from pipeline.models import Bar

BASE_URL = "https://comidadibuteco.com.br/butecos/"


def _label_value(soup: BeautifulSoup, pattern: str) -> str | None:
    """Return text following a <b> label matching pattern, within the same parent."""
    b_tag = soup.find("b", string=re.compile(pattern, re.IGNORECASE))
    if not b_tag:
        return None
    parent_text = b_tag.parent.get_text(strip=True)
    label_text = b_tag.get_text(strip=True)
    value = parent_text.replace(label_text, "", 1).strip()
    return value or None


def parse_bar_links_and_next(html: str) -> tuple[list[str], str | None]:
    """Return (detail_urls, next_page_url_or_None) from a listing page."""
    soup = BeautifulSoup(html, "html.parser")
    links = [
        a["href"]
        for a in soup.find_all("a", role="link")
        if a.get_text(strip=True) == "Detalhes" and a.get("href")
    ]
    next_el = soup.select_one("a.next.page-link")
    next_url = next_el["href"] if next_el and next_el.get("href") else None
    return links, next_url


def parse_bar_detail(html: str, url: str) -> Bar:
    """Extract all bar fields from a detail page."""
    soup = BeautifulSoup(html, "html.parser")

    name_el = soup.select_one("h1.section-title")
    name = name_el.get_text(strip=True) if name_el else ""

    address = _label_value(soup, r"Endere[cç]o")
    parsed_address = parse_address(address)

    section_div = soup.select_one("div.section-text")
    food_name = None
    food_description = None
    if section_div:
        first_p = section_div.find("p")
        if first_p:
            b_tag = first_p.find("b")
            if b_tag:
                food_name = b_tag.get_text(strip=True)
                full_text = first_p.get_text(strip=True)
                food_description = full_text.replace(food_name, "", 1).strip() or None

    img_el = soup.select_one("img.img-fluid.img-single.wp-post-image")
    food_image_url = img_el.get("src") if img_el else None

    working_hours = _label_value(soup, r"Hor[aá]rio")

    return Bar(
        name=name,
        address=address,
        street=parsed_address["street"],
        street_number=parsed_address["street_number"],
        complement=parsed_address["complement"],
        neighborhood=parsed_address["neighborhood"],
        city=parsed_address["city"],
        state=parsed_address["state"],
        food_name=food_name,
        food_image_url=food_image_url,
        food_description=food_description,
        working_hours=working_hours,
        detail_url=url,
    )


async def _get_html(page: Page, url: str) -> str:
    await page.goto(url, wait_until="domcontentloaded")
    await page.wait_for_timeout(800)
    return await page.content()


async def scrape_all(delay_ms: int = 1000) -> AsyncGenerator[Bar, None]:
    """Async generator: yields one Bar per buteco, paginating through all listing pages."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            channel="chrome",
            headless=True,
            args=["--disable-blink-features=AutomationControlled"],
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720},
        )
        page = await context.new_page()
        current_url: str | None = BASE_URL

        while current_url:
            html = await _get_html(page, current_url)
            detail_urls, next_url = parse_bar_links_and_next(html)

            for detail_url in detail_urls:
                try:
                    detail_html = await _get_html(page, detail_url)
                    bar = parse_bar_detail(detail_html, detail_url)
                    yield bar
                except Exception as exc:
                    print(f"[SKIP] {detail_url} — {exc}")
                await page.wait_for_timeout(delay_ms)

            current_url = next_url

        await browser.close()
