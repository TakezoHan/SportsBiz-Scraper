"""
Output formatter — writes classified activations to daily_audit.json.
"""

import json
import logging
import os
from datetime import date, datetime

logger = logging.getLogger(__name__)

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))


def build_audit_entry(result) -> dict:
    """Convert a ClassificationResult into the daily_audit schema."""
    return {
        "date": date.today().isoformat(),
        "property": result.property,
        "activity_type": result.activity_type,
        "country": result.country,
        "summary": result.summary,
        "source": result.source_name,
        "source_url": result.source_url,
        "headline": result.headline,
        "confidence": result.confidence,
    }


def write_daily_audit(results: list, output_path: str | None = None) -> str:
    """
    Write the list of ClassificationResult objects to a dated JSON file.

    Returns the path of the written file.
    """
    if output_path is None:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        filename = f"daily_audit_{timestamp}.json"
        output_path = os.path.join(OUTPUT_DIR, filename)

    entries = [build_audit_entry(r) for r in results]

    audit = {
        "generated_at": datetime.now().isoformat(),
        "total_activations": len(entries),
        "activations": entries,
    }

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(audit, f, indent=2)

    logger.info("Daily audit written to %s (%d entries)", output_path, len(entries))
    return output_path
