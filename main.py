#!/usr/bin/env python3
"""
SportsBiz Scraper — Multi-Source Sports Marketing Activation Auditor.

Usage:
    python main.py                  # scrape all sources
    python main.py --sources sportspro,frontofficesports  # specific sources only
    python main.py --dry-run        # scrape only, skip classification (no API cost)
"""

import argparse
import asyncio
import json
import logging
import os
import sys
from datetime import date
from pathlib import Path

from dotenv import load_dotenv

from scraper.engine import run_scraper
from filters.classifier import classify_batch
from output.formatter import write_daily_audit

load_dotenv()

ROOT = Path(__file__).resolve().parent
SOURCES_PATH = ROOT / "config" / "sources.json"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("sportsbiz")


REQUIRED_SOURCE_KEYS = {"id", "name", "url", "type", "selectors"}
REQUIRED_SELECTOR_KEYS = {"article_links", "headline", "body"}


def load_sources(filter_ids: list[str] | None = None) -> list[dict]:
    with open(SOURCES_PATH) as f:
        data = json.load(f)

    sources = data["sources"]
    if filter_ids:
        sources = [s for s in sources if s["id"] in filter_ids]

    if not sources:
        logger.error("No sources matched the filter. Check --sources flag.")
        sys.exit(1)

    # Validate each source has required keys
    for src in sources:
        missing = REQUIRED_SOURCE_KEYS - src.keys()
        if missing:
            logger.error("Source '%s' missing keys: %s", src.get("id", "?"), missing)
            sys.exit(1)
        sel_missing = REQUIRED_SELECTOR_KEYS - src["selectors"].keys()
        if sel_missing:
            logger.error("Source '%s' selectors missing: %s", src["id"], sel_missing)
            sys.exit(1)

    return sources


def main():
    parser = argparse.ArgumentParser(
        description="Scrape sports-business sites and classify marketing activations."
    )
    parser.add_argument(
        "--sources",
        type=str,
        default=None,
        help="Comma-separated source IDs to scrape (default: all)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Scrape articles but skip Claude classification (no API cost)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Custom output path for daily_audit.json",
    )
    args = parser.parse_args()

    filter_ids = args.sources.split(",") if args.sources else None
    sources = load_sources(filter_ids)

    logger.info("Starting scrape of %d source(s)...", len(sources))
    for s in sources:
        logger.info("  - %s (%s)", s["name"], s["url"])

    # --- Scrape ---
    articles = asyncio.run(run_scraper(sources))

    if not articles:
        logger.warning("No articles scraped. Check network / selectors.")
        sys.exit(0)

    logger.info("Scraped %d articles total.", len(articles))

    if args.dry_run:
        logger.info("--dry-run: dumping raw headlines to stdout")
        for a in articles:
            print(f"[{a.source_id}] {a.headline}")
        sys.exit(0)

    # --- Classify ---
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        logger.error(
            "ANTHROPIC_API_KEY not set. Export it or add to .env. "
            "Use --dry-run to scrape without classification."
        )
        sys.exit(1)

    activations = classify_batch(articles, api_key=api_key)

    if not activations:
        logger.info("No marketing activations found in today's scrape.")
        sys.exit(0)

    # --- Output ---
    path = write_daily_audit(activations, output_path=args.output)
    logger.info("Done. Audit saved to: %s", path)

    # Print a quick summary to terminal
    print("\n=== DAILY ACTIVATION AUDIT ===")
    print(f"Date: {date.today().isoformat()}")
    print(f"Activations found: {len(activations)}\n")
    for i, a in enumerate(activations, 1):
        print(f"  {i}. [{a.property}] {a.activity_type} — {a.country}")
        print(f"     {a.summary}")
        print(f"     Source: {a.source_url}\n")


if __name__ == "__main__":
    main()
