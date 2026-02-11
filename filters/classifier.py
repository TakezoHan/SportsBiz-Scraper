"""
Contextual filter / classification engine.

Uses Anthropic's Claude API to decide whether a scraped article
represents a *Marketing / Physical Activation* (the signal) vs
*General News* (noise), and to extract structured fields for the
daily audit.
"""

import json
import logging
import os
import time
from dataclasses import dataclass

from anthropic import Anthropic

logger = logging.getLogger(__name__)

CLASSIFICATION_PROMPT = """\
You are a sports-business intelligence analyst specializing in
international sports marketing activations.

TARGET PROPERTIES: F1, NBA, NFL, Premier League clubs, La Liga clubs,
Bundesliga clubs, Serie A clubs.

TARGET MARKETS: India, KSA (Saudi Arabia), UAE, Japan.

ACTIVATION TYPES (what counts as "Marketing / Physical Activation"):
- VIP hospitality events or fan experiences in a target market
- Grassroots sports clinics, youth camps, or coaching programmes
- Marketing pop-ups, brand activations, or roadshows
- Pre-season tours, exhibition matches, or friendlies held in a target market
- Sponsorship launches tied to a physical event in a target market
- eSports watch-parties or gaming events organised in a target market

WHAT DOES NOT COUNT:
- General match results, player transfers, or injury news
- TV broadcast deals with no physical activation component
- Social-media-only campaigns with no on-the-ground element
- Internal league governance or regulatory news

---

Analyse the article below and return ONLY a JSON object (no markdown
fences) with these fields:

{
  "is_activation": true/false,
  "confidence": 0.0-1.0,
  "property": "name of the sports property (e.g. 'NBA', 'Manchester City', 'F1')",
  "activity_type": "one of: VIP Event | Grassroots Clinic | Marketing Activation | Exhibition Match | Sponsorship Launch | Fan Experience | Other",
  "country": "target market country or 'N/A'",
  "summary": "2-sentence summary of the activation"
}

If the article is NOT a relevant activation, set is_activation=false
and leave property/activity_type/country/summary as "N/A".

ARTICLE SOURCE: {source_name}
HEADLINE: {headline}
BODY (truncated):
{body}
"""


@dataclass
class ClassificationResult:
    is_activation: bool
    confidence: float
    property: str
    activity_type: str
    country: str
    summary: str
    source_url: str
    source_name: str
    headline: str


def _build_prompt(article) -> str:
    return CLASSIFICATION_PROMPT.format(
        source_name=article.source_name,
        headline=article.headline,
        body=article.body[:2500],
    )


MAX_RETRIES = 2
RATE_LIMIT_DELAY = 1.0  # seconds between API calls


def classify_article(client: Anthropic, article) -> ClassificationResult | None:
    """Send a single article through Claude for classification (with retry)."""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=512,
                messages=[
                    {"role": "user", "content": _build_prompt(article)},
                ],
            )

            raw = response.content[0].text.strip()

            # Handle potential markdown fences in response
            if raw.startswith("```"):
                raw = raw.split("\n", 1)[1]
                raw = raw.rsplit("```", 1)[0]

            data = json.loads(raw)
            confidence = min(max(float(data.get("confidence", 0)), 0.0), 1.0)

            return ClassificationResult(
                is_activation=data.get("is_activation", False),
                confidence=confidence,
                property=data.get("property", "N/A"),
                activity_type=data.get("activity_type", "N/A"),
                country=data.get("country", "N/A"),
                summary=data.get("summary", "N/A"),
                source_url=article.url,
                source_name=article.source_name,
                headline=article.headline,
            )
        except json.JSONDecodeError as e:
            logger.warning(
                "Attempt %d: Claude returned non-JSON for '%s': %s",
                attempt, article.headline, e,
            )
            if attempt < MAX_RETRIES:
                time.sleep(RATE_LIMIT_DELAY * attempt)
                continue
            return None
        except Exception as e:
            logger.error(
                "Attempt %d: Classification failed for '%s': %s",
                attempt, article.headline, e,
            )
            if attempt < MAX_RETRIES:
                time.sleep(RATE_LIMIT_DELAY * attempt)
                continue
            return None
    return None


def classify_batch(articles: list, api_key: str | None = None) -> list[ClassificationResult]:
    """
    Classify a list of Article objects.  Returns only those that
    passed the activation filter (is_activation=True, confidence >= 0.6).
    """
    key = api_key or os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        raise RuntimeError(
            "ANTHROPIC_API_KEY not set. Export it or add to .env file."
        )

    client = Anthropic(api_key=key)
    results: list[ClassificationResult] = []

    consecutive_failures = 0
    for i, article in enumerate(articles, 1):
        logger.info(
            "Classifying [%d/%d]: %s", i, len(articles), article.headline[:80]
        )
        result = classify_article(client, article)

        # Rate-limit between calls
        time.sleep(RATE_LIMIT_DELAY)

        if result is None:
            consecutive_failures += 1
            if consecutive_failures >= 5:
                logger.error("Circuit breaker: 5 consecutive failures, aborting batch.")
                break
        else:
            consecutive_failures = 0

        if result and result.is_activation and result.confidence >= 0.6:
            results.append(result)
            logger.info(
                "  -> ACTIVATION: %s | %s | %s (%.0f%%)",
                result.property,
                result.activity_type,
                result.country,
                result.confidence * 100,
            )
        else:
            logger.debug("  -> filtered out (general news)")

    logger.info(
        "Classification complete: %d activations from %d articles",
        len(results),
        len(articles),
    )
    return results
