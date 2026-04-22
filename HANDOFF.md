# HANDOFF: SportsBiz Multi-Source Marketing Scraper

**Created:** 2026-04-22
**Branch:** `claude/sports-marketing-scraper-H7xjd`
**Repo:** `TakezoHan/SportsBiz-Scraper`
**Status:** Functional scaffold, not yet production-tested against live sites

---

## What This Project Does

Automates "Global Benchmarking" by scraping sports business news sites,
then using Claude's API to classify which articles represent **physical
marketing activations** (VIP events, grassroots clinics, fan experiences,
exhibition matches) vs general sports news.

**Target properties:** F1, NBA, NFL, Premier League, La Liga, Bundesliga, Serie A
**Target markets:** India, KSA, UAE, Japan

---

## Architecture

```
main.py                    CLI orchestrator (argparse)
  |
  +-- scraper/engine.py    Playwright async scraper (headless Chromium)
  |                        - Concurrent: one browser context per source
  |                        - Deduplicates URLs across all sources
  |                        - Max 15 articles per source
  |                        - 30s timeout per page
  |
  +-- filters/classifier.py  Claude API classification engine
  |                        - Model: claude-sonnet-4-20250514
  |                        - 1s rate-limit between API calls
  |                        - Retry: 2 attempts with exponential backoff
  |                        - Circuit breaker: aborts after 5 consecutive failures
  |                        - Confidence threshold: >= 0.6 to pass filter
  |
  +-- output/formatter.py  Writes timestamped daily_audit_YYYY-MM-DD_HHMMSS.json
  |
  +-- config/sources.json  Modular source registry (add/remove, no code change)
```

### Data Flow

```
sources.json -> Playwright scrapes index pages -> extracts article links
-> scrapes each article (headline + body) -> deduplicates
-> sends each to Claude for classification -> filters activations (>=60% confidence)
-> writes daily_audit.json
```

---

## Files

| File | Purpose | Lines |
|------|---------|-------|
| `main.py` | CLI entry point, validation, orchestration | 144 |
| `scraper/engine.py` | Async Playwright scraper, Article dataclass | 155 |
| `filters/classifier.py` | Claude API classifier, prompt, retry logic | 195 |
| `output/formatter.py` | JSON output writer | 54 |
| `config/sources.json` | 6 sources with CSS selectors | 81 |
| `mock_daily_audit.json` | Example output for Excel import testing | 72 |
| `requirements.txt` | playwright, anthropic, python-dotenv | 3 |
| `.env.example` | Template for ANTHROPIC_API_KEY | 1 |
| `.gitignore` | Excludes .env, __pycache__, output/*.json | 4 |

---

## Sources (6 total)

| ID | Name | Why |
|----|------|-----|
| `sportspro` | SportsPro Media | Industry leader for sponsorship/activation coverage |
| `sportbusiness` | SportBusiness | Premium intel on commercial deals, international expansion |
| `frontofficesports` | Front Office Sports | NBA/NFL international strategy, grassroots |
| `insideworldfootball` | Inside World Football | UEFA/FIFA club commercial ops, Asia/ME activations |
| `arabianbusiness_sport` | Arabian Business - Sport | On-the-ground KSA/UAE activations |
| `laliga_biz` | LaLiga Official News | LaLiga international expansion, fan events |

### How to Add a Source

Append to the `sources` array in `config/sources.json`:
```json
{
  "id": "your_id",
  "name": "Display Name",
  "url": "https://example.com/news",
  "type": "js_heavy",
  "why": "Reason for including",
  "selectors": {
    "article_links": "a[href*='/news/']",
    "headline": "h1",
    "body": "div.article-body"
  }
}
```
Selectors are CSS. Inspect the target site in DevTools to find them.

---

## CLI Usage

```bash
python main.py                                      # full run (all sources)
python main.py --sources sportspro,laliga_biz       # specific sources only
python main.py --dry-run                            # scrape only, no API cost
python main.py --output ./my_audit.json             # custom output path
```

---

## Output Schema (daily_audit.json)

```json
{
  "generated_at": "2026-04-22T09:30:00",
  "total_activations": 3,
  "activations": [
    {
      "date": "2026-04-22",
      "property": "NBA",
      "activity_type": "Grassroots Clinic",
      "country": "India",
      "summary": "Two sentences describing the activation.",
      "source": "Front Office Sports",
      "source_url": "https://...",
      "headline": "Article headline",
      "confidence": 0.95
    }
  ]
}
```

Activity types: `VIP Event` | `Grassroots Clinic` | `Marketing Activation` | `Exhibition Match` | `Sponsorship Launch` | `Fan Experience` | `Other`

---

## Known Issues and Limitations

### Must address before production use

1. **CSS selectors are fragile.** They will break when sites redesign. Plan to
   re-inspect and update `sources.json` selectors periodically.
2. **No caching.** Running twice on the same day re-scrapes everything and
   re-classifies every article (duplicate API cost).
3. **Classification is synchronous.** Fine for <50 articles. At scale, consider
   batching or async classification.
4. **No article publication date.** The `date` field is the scrape date, not when
   the article was published. Scraper doesn't extract pub dates.
5. **Single static user-agent.** Heavy use may get rate-limited or blocked.
   Consider user-agent rotation.
6. **Front Office Sports selector** `a[href*='/20']` matches year in URL path;
   will break for articles from 2030+.
7. **Body double-truncation.** Scraped at 3000 chars, then re-truncated to 2500
   before classification. Not harmful but wasteful.

### Design decisions worth revisiting

- Confidence threshold of 0.6 is a starting point. Tune after reviewing a few
  real runs to see false-positive/false-negative rate.
- `MAX_ARTICLES_PER_SOURCE = 15` is conservative. Increase if a source publishes
  heavily.
- The prompt lists "Premier League clubs" generically. If you only care about
  specific clubs (e.g. Man City, Arsenal), narrow the prompt.

---

## Configuration / Environment

**Required:**
- Python 3.11+
- `ANTHROPIC_API_KEY` in `.env` file or environment variable

**Dependencies:**
```
playwright>=1.40.0
anthropic>=0.39.0
python-dotenv>=1.0.0
```

**Playwright browser install** (one-time):
```bash
playwright install chromium
```

---

## Commit History

```
ad71732  Initialize multi-source sports marketing scraper
c8cbdca  Fix critical bugs from audit + add LaLiga source + mock output
```

### What was fixed in the audit (commit c8cbdca):
- `main.py:119` printed source_name instead of date -> fixed to `date.today()`
- Added `REQUIRED_SOURCE_KEYS` / `REQUIRED_SELECTOR_KEYS` validation
- Cross-source URL deduplication in `run_scraper()`
- Rate limiting (1s delay), retry (2 attempts), circuit breaker (5 failures)
- Confidence clamped to [0.0, 1.0]
- Removed unused `beautifulsoup4` dependency

---

## For Your Next Claude Session

Paste this to bring a new session up to speed:

> I have a Python project called SportsBiz-Scraper in my Cowork folder.
> It scrapes sports business news sites using Playwright (headless Chromium)
> and classifies articles as marketing activations vs general news using
> Claude's API (claude-sonnet-4-20250514). The output is a daily_audit.json.
>
> Architecture: main.py orchestrates scraper/engine.py (async Playwright),
> filters/classifier.py (Claude API with rate limiting and circuit breaker),
> and output/formatter.py. Sources are configured in config/sources.json
> (6 sources: SportsPro, SportBusiness, FOS, InsideWorldFootball,
> ArabianBusiness, LaLiga Official).
>
> Known issues: CSS selectors are fragile, no caching between runs, no
> article pub-date extraction, synchronous classification loop.
> See HANDOFF.md for full details.
