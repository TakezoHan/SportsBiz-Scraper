"""
Playwright-based scraper engine.

Handles both JS-heavy (SPA) and static sites through a single
async Playwright pipeline. Each source from sources.json is
scraped for article links, then individual articles are fetched
and their text content extracted.
"""

import asyncio
import logging
from dataclasses import dataclass, field
from playwright.async_api import async_playwright, Browser, Page

logger = logging.getLogger(__name__)

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)

# Hard ceiling so a single run doesn't explode
MAX_ARTICLES_PER_SOURCE = 15
PAGE_TIMEOUT_MS = 30_000


@dataclass
class Article:
    source_id: str
    source_name: str
    url: str
    headline: str
    body: str
    raw_html: str = ""
    extra: dict = field(default_factory=dict)


async def _extract_article_links(page: Page, source: dict) -> list[str]:
    """Return absolute URLs matching the source's article_links selector."""
    selector = source["selectors"]["article_links"]
    elements = await page.query_selector_all(selector)

    urls: list[str] = []
    for el in elements:
        href = await el.get_attribute("href")
        if not href:
            continue
        # Resolve relative URLs
        if href.startswith("/"):
            from urllib.parse import urljoin
            href = urljoin(source["url"], href)
        if href not in urls:
            urls.append(href)

    return urls[:MAX_ARTICLES_PER_SOURCE]


async def _scrape_article(page: Page, url: str, source: dict) -> Article | None:
    """Navigate to a single article URL and extract headline + body."""
    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=PAGE_TIMEOUT_MS)
        await page.wait_for_timeout(1500)  # let JS hydrate

        selectors = source["selectors"]

        # Headline
        headline = ""
        for sel in selectors["headline"].split(", "):
            el = await page.query_selector(sel)
            if el:
                headline = (await el.inner_text()).strip()
                break

        # Body text
        body = ""
        for sel in selectors["body"].split(", "):
            el = await page.query_selector(sel)
            if el:
                body = (await el.inner_text()).strip()
                break

        if not headline and not body:
            logger.debug("No content extracted from %s", url)
            return None

        return Article(
            source_id=source["id"],
            source_name=source["name"],
            url=url,
            headline=headline,
            body=body[:3000],  # cap body to keep token costs sane
        )
    except Exception as e:
        logger.warning("Failed to scrape %s: %s", url, e)
        return None


async def scrape_source(browser: Browser, source: dict) -> list[Article]:
    """Scrape a single source: find article links, then scrape each one."""
    context = await browser.new_context(user_agent=USER_AGENT)
    page = await context.new_page()
    articles: list[Article] = []

    try:
        logger.info("Scraping index: %s (%s)", source["name"], source["url"])
        await page.goto(source["url"], wait_until="domcontentloaded", timeout=PAGE_TIMEOUT_MS)
        await page.wait_for_timeout(2000)

        links = await _extract_article_links(page, source)
        logger.info("Found %d article links on %s", len(links), source["name"])

        for link_url in links:
            article = await _scrape_article(page, link_url, source)
            if article:
                articles.append(article)

    except Exception as e:
        logger.error("Source %s failed: %s", source["id"], e)
    finally:
        await context.close()

    return articles


async def run_scraper(sources: list[dict]) -> list[Article]:
    """
    Main entry point.  Launches a headless Chromium browser, scrapes every
    source concurrently (one browser context per source), and returns
    all extracted articles.
    """
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        try:
            tasks = [scrape_source(browser, src) for src in sources]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            articles: list[Article] = []
            for result in results:
                if isinstance(result, list):
                    articles.extend(result)
                elif isinstance(result, Exception):
                    logger.error("Source task failed: %s", result)

            logger.info("Total articles scraped: %d", len(articles))
            return articles
        finally:
            await browser.close()
