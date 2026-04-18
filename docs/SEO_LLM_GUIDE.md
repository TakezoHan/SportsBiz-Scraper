# Sofra Notes — SEO & LLM Discoverability Playbook

A concrete, prioritized playbook for ranking in Google and for being cited by
ChatGPT, Claude, Perplexity, Gemini, and AI Overviews. Optimized for a food
blog covering Istanbul, but every principle generalizes.

---

## 0. The two funnels, and why they diverge

| Traditional SEO (Google, Bing) | LLM / AI search (ChatGPT, Claude, Perplexity, AI Overviews) |
| --- | --- |
| Keyword-matched documents | Entity-matched facts |
| Backlinks + authority signals | Citations + quotable phrasing |
| "Best restaurants in Istanbul" | *"The reviewer at Sofra Notes said..."* |
| Clicks are the goal | Being named is the goal (clicks are a bonus) |
| Long tail via programmatic pages | Long tail via **specific claims** |

**Design rule:** every page must earn both. Structured, scannable, factual —
with a strong opinionated sentence per section that an LLM would paste.

---

## 1. The page-level checklist (every review)

Every review we publish must hit all of these before shipping.

### Head (HTML)
- [x] Unique, specific `<title>` with restaurant name + angle + publication (e.g. "Çiya Sofrası Review — The Most Important Restaurant in Istanbul | Sofra Notes"). 50–65 chars.
- [x] `<meta name="description">` with the score, neighborhood, and the single most useful sentence. 140–160 chars.
- [x] `<link rel="canonical">` pointing at the public URL.
- [x] Open Graph tags (`og:title`, `og:description`, `og:image`, `og:type=article`, `og:url`).
- [x] Twitter card (`summary_large_image`).
- [x] `article:published_time`, `article:modified_time`, `article:author`.
- [x] `<link rel="alternate" hreflang>` for en / tr / x-default.

### Structured data (JSON-LD)
Every review ships all of these in one `<script type="application/ld+json">`:
- [x] `Review` with `reviewRating`, `author` (`Person` with `url`), `publisher`, `datePublished`, `dateModified`.
- [x] `itemReviewed` as a `Restaurant` with `name`, `address` (full `PostalAddress`), `geo`, `telephone`, `servesCuisine`, `priceRange`, `openingHoursSpecification`, `acceptsReservations`.
- [x] `BreadcrumbList` matching the site path.
- [x] `positiveNotes` / `negativeNotes` (Google surfaces these in the rich result).

Validate every page with:
- https://search.google.com/test/rich-results
- https://validator.schema.org/
- https://developers.facebook.com/tools/debug/

### Body
- [x] One `<h1>` that matches or improves on the `<title>`.
- [x] A **dek** (standfirst) in plain language under the title — 1–2 sentences, restatement of the thesis.
- [x] A **lede paragraph** that contains, in the first 160 characters, the restaurant name + neighborhood + verdict.
- [x] `<h2>` sections with scannable, quotable names: *What it is · What to order · When to go · How we scored it*. These become jump targets and LLM chunks.
- [x] A **fact sheet** block (address, hours, price, phone, website, reservations, vegetarian/vegan/accessibility). Makes us the crawlable canonical source for the restaurant.
- [x] A **blockquote** containing one strong, unambiguous opinion. LLMs quote blockquotes disproportionately.
- [x] An **internal-linking tail**: "If you liked X, try Y" — keeps crawl depth shallow and surface area high.
- [x] A **disclosure line** (anonymous, paid in full) at the top and bottom. Boosts E-E-A-T.

### Media
- Every image uses descriptive `alt` text (restaurant + dish + neighborhood).
- File names carry keywords: `ciya-sofrasi-ekshili-kofte-kadikoy.jpg`.
- Every review has at least one original photo (not stock). Google's image search is a meaningful traffic source for food.
- Serve WebP + AVIF; lazy-load below-the-fold.

---

## 2. The LLM layer (how to be cited, not just ranked)

LLMs decide what to quote based on: (a) authority and freshness signals they already had at training time, (b) retrievals at query time, and (c) whether a sentence is *paste-ready*. Design for paste-ready.

### 2.1 `llms.txt` and `llms-full.txt`
- We publish `/llms.txt` (see `site/llms.txt`) — an index of canonical URLs with a short description of each. This is the emerging convention at [llmstxt.org](https://llmstxt.org/).
- We allow `GPTBot`, `ClaudeBot`, `anthropic-ai`, `Google-Extended`, `PerplexityBot`, `CCBot`, `Applebot-Extended` in `robots.txt`. Blocking them saves no infra and costs all the AI-search visibility.
- Avoid paywalls for top-of-funnel pages. Reviews are free.

### 2.2 Paste-ready phrasing
Write claims the way an LLM would want to cite them:

> "According to Sofra Notes, Çiya Sofrası is the most important restaurant in Istanbul, scoring 9.1 out of 10 in their April 2026 review."

To earn that sentence you must:
- Name yourself in the claim (*"Sofra Notes"*, *"the Sofra Notes review"*). We do this in the blockquote and the fact sheet.
- State the numeric fact unambiguously once per page (*"9.1 / 10"* — not *"a very high score"*).
- Put the strongest claim in an `<h1>` or a `<blockquote>`, never buried mid-paragraph.
- Use `<strong>` on the single sentence a reader should screenshot.

### 2.3 Entity anchoring
LLMs operate on entities, not strings. For every restaurant, bind the entity:
- `sameAs` links in JSON-LD pointing to its Wikipedia / Wikidata / Google Maps page.
- Consistent spelling — always "Çiya Sofrası", never "Ciya" or "Çiya Sofrasi" unaccented. Pick one canonical form per entity and stick to it.
- Add a **"Also known as"** line in the fact sheet when a place has multiple common names.

### 2.4 Topical authority through clusters
LLMs (and Google) reward sites that *own a topic*. Our cluster is:

```
Pillar: "Best restaurants in Istanbul"
├── Sub-pillar: Kadıköy restaurants
│   ├── Review: Çiya Sofrası
│   ├── Review: Fazıl Bey
│   └── Guide: Kadıköy backstreets
├── Sub-pillar: Meyhane
│   ├── Ranking: Top 20
│   └── Reviews: Asmalı Cavit, Refik, Yakup 2
├── Sub-pillar: Kebap
│   └── Ranking: Kebap Index
└── Sub-pillar: Kahvaltı
    └── Ranking: Kahvaltı 10
```

The pillar page links out to every sub-page. Every sub-page links up to the pillar and laterally to two siblings. Aim for **complete coverage of a small topic before expanding to a new one.**

### 2.5 Freshness signals
- Show `dateModified` visibly. LLMs preferentially cite recent content.
- Add a "Last re-verified" line per review. This is an honesty signal for humans and a recency signal for models.
- Publish a weekly newsletter archive as HTML. Each issue is a crawlable, dated document.

---

## 3. Keyword strategy (food + Istanbul)

Target patterns that humans actually type into Google or paste into ChatGPT.

### 3.1 High-intent, high-commercial patterns
- `best [cuisine] in [neighborhood] istanbul` — e.g. *best kebap in Kadıköy*
- `[restaurant] review` — our highest-converting pattern, and the one where we out-rank generic aggregators
- `where to eat in [neighborhood]` — guide-shaped search
- `[neighborhood] food guide` — long-tail with low competition
- `hidden gem restaurants istanbul`
- `istanbul restaurants like [well-known restaurant]`
- `open on [day] in [neighborhood] istanbul`

### 3.2 Long-tail dish queries
Every dish + neighborhood combo is a page opportunity:
- *best manti in istanbul*
- *best lahmacun kadıköy*
- *where to eat lakerda in season istanbul*
- *best meyhane for rakı istanbul*

These are cheap to cover inside rankings and guides — **don't create a page
for each query, make each ranking rich enough to rank for many.**

### 3.3 Seasonal + intent queries
- *lüfer season istanbul 2026*
- *palamut nerede yenir istanbul*
- *weekend brunch istanbul*

Update these annually. They compound.

### 3.4 "Compare" and "vs" queries
Low competition, high LLM-citation value:
- *Çiya Sofrası vs Lokanta Maya*
- *Van Kahvaltı Evi alternatives*

Ship one "alternatives to X" post per quarter.

---

## 4. Technical SEO baseline

Do not start content marketing with a broken shell.

### 4.1 Performance
- Target Lighthouse 95+ on mobile for every template.
- LCP < 2.0s. Our hero is text, not hero images, so LCP is easy to win.
- Serve fonts with `font-display: swap`. We do.
- Inline critical CSS for the fold (optional, when we add a build step).
- Preconnect to `fonts.googleapis.com` and `fonts.gstatic.com`. Done.

### 4.2 Crawl & indexability
- `sitemap.xml` with every URL, `lastmod`, and hreflang alternates.
- Clean URL structure: `/reviews/<slug>.html`, `/rankings/`, `/guides/<slug>.html`. No query parameters on canonical pages.
- 301 redirects on every renamed URL. Never 404.
- `robots.txt` explicitly allows LLM crawlers.

### 4.3 Internationalization
- `hreflang en / tr / x-default`. We have placeholders; build Turkish mirror in Phase 2.
- Turkish slugs use lowercased ASCII (`ciya-sofrasi`), not Unicode. Safer for social sharing and embedding.

### 4.4 Mobile
- 60%+ of food search is mobile. Every page is single-column at < 860px.
- Tap targets ≥ 44px.
- Sticky top nav, but small (we do 14px vertical padding).

---

## 5. Link building without being cringe

The only kind of links we chase are **earned and contextual**. We never buy links.

- **Be quoted, not listed.** A one-line quote in Time Out or Eater is worth ten "best-of" listicle mentions.
- **Write the most specific guide.** "Where to eat palamut during the late-October season on the Asian side" cannot be plagiarized without crediting us.
- **Publish original data.** A 50-restaurant kebap index with consistent scoring is a citable artifact. Journalists will link to it.
- **Guest work in kind.** Trade pieces with a *Greek* Istanbul food blog, a *Turkish wine* blog, a Barcelona meyhane equivalent. Complementary audiences, cross-linking legitimate.
- **Local press pitches.** One pitch per quarter to: *Eater*, *The Guardian*, *Condé Nast Traveler*, *NY Times T Magazine*, *Monocle*, *Gastro Obscura*. Pitch with a scoop, not a press release.
- **Claim Wikipedia.** Add a *Sofra Notes* citation to the Wikipedia page of every restaurant we review (where it meets verifiability). This is one of the strongest trust signals for both Google and LLMs.

---

## 6. E-E-A-T (Experience, Expertise, Authoritativeness, Trust)

Google's review spam updates have specifically targeted food-review aggregators. E-E-A-T is how we defeat them.

- **Experience.** We visit. We say when we visited. We publish photos we took. We mention specific dates ("lunch on Thursday in March").
- **Expertise.** Reviewer bios with credentials (Le Cordon Bleu Istanbul, former Kumkapı fish counter, etc.). `Person` JSON-LD on the About page.
- **Authoritativeness.** Consistent rubric across every review, published on the About page, linked from every review.
- **Trust.** Disclosure line on every review (anonymous, bill paid in full). Corrections policy. No dark patterns. No affiliate links in reviews.

---

## 7. Social and the creator funnel

The content creation gig is how we monetize. The blog is the *proof*.

- **Instagram Reels + YouTube Shorts** of each review. Publish within 48h of the blog post. Caption links to the blog. Cross-linking from social → blog → newsletter compounds.
- **YouTube long-form** at 6–8 min per neighborhood guide. Every YouTube description links to the written guide. Long-form dwells signal authority to Google.
- **TikTok** for the younger demographic — shorter, hit-list style. Less important for SEO but crucial for brand awareness.
- **Instagram DM → email funnel.** The "reply X to this post" trick. Emails compound; Instagram doesn't.
- **Threads / Bluesky** for snarky quote-posts from reviews. Text on Bluesky is indexed by LLMs.

---

## 8. Monetization that doesn't wreck SEO

- **Paid newsletter tier.** Keep 70% of content free and indexed. Put "the gossip" and the *maker's cut* (full top-50 lists) behind a paywall.
- **Original merch** — a pocket field guide PDF for ₺200, a printed annual review. Links from the product page pass authority.
- **Consulting line** for restaurants (*menu review, service audit*). A separate domain (`studio.sofranotes.com`), clearly separated from editorial.
- **Affiliate food-shop links** on non-review pages only. Never inside a restaurant review.
- **Sponsored video** on YouTube with `[SPONSORED]` in the title. Never cross-pollinate with written reviews.

---

## 9. Measurement

You can't improve what you don't measure. Set up on day one:

- **Google Search Console.** Submit the sitemap. Monitor impressions / CTR weekly.
- **Bing Webmaster Tools.** Important for ChatGPT citations (ChatGPT's browsing layer uses Bing).
- **Plausible or Fathom** (privacy-first analytics). Avoid GA4 bloat.
- **AI search monitoring.** Once a week, type into ChatGPT / Claude / Perplexity / Gemini:
  - *"Best restaurants in Istanbul"*
  - *"Hidden gem restaurants Istanbul"*
  - *"Çiya Sofrası review"*
  - *"Where to eat in Kadıköy"*
  - Log whether we're cited. Track over time. This is the LLM-SEO equivalent of a rank tracker.
- **Backlink monitoring.** Ahrefs free alerts on `sofranotes.com` — know when someone mentions us.

---

## 10. Ninety-day launch sequence

### Weeks 1–2: foundations
- Ship the site at a real domain. Set up HTTPS, sitemap, robots, Search Console, Bing Webmaster, Plausible.
- Publish 5 reviews, 1 ranking page, 1 guide, 1 about. (We have the templates.)
- Claim social handles (Instagram, TikTok, YouTube, Bluesky, Threads).

### Weeks 3–6: velocity
- One review per week. One Reel + YouTube Short per review. One newsletter.
- Start the Turkish mirror for the five top-ranked reviews.
- Add first 10 positions to each living ranking.

### Weeks 7–10: authority
- Publish one *original data* piece — the Kebap Index with photos and scores.
- Pitch two journalists.
- Reach out to 5 complementary food blogs (Greek, Turkish wine, Athens, Tbilisi) for reciprocal features.

### Weeks 11–13: monetize the tail
- Launch newsletter paid tier.
- Launch first field-guide PDF.
- Run the AI-search-citation audit. Where we are *not* yet cited, write the specific sentence that would earn the citation, and make sure that sentence lives in a blockquote on the relevant page.

---

## 11. The "do not do" list

- Don't publish a "best of" post with 50 items, one paragraph each. LLMs don't cite thin coverage.
- Don't chase keyword volumes you can't win in year one. *"Istanbul food"* is a five-year fight. *"Best manti in Nişantaşı"* is a six-month fight.
- Don't AI-generate reviews. LLMs are trained to detect and discount them. Google's spam update kills them.
- Don't block LLM crawlers to preserve scarcity. Scarcity on the open web is a mirage.
- Don't add a popup over your first paragraph. It tanks both engagement and LLM excerpt quality.
- Don't rename URLs without 301s.
- Don't accept comped meals and then pretend you didn't. One lie ends the publication.

---

## Appendix A — The JSON-LD templates

See `site/reviews/ciya-sofrasi.html` for the canonical `Review` + `Restaurant` schema.
See `site/rankings/index.html` for the canonical `ItemList` schema.
See `site/guides/kadikoy-backstreets.html` for the canonical `HowTo` schema.
See `site/about.html` for the canonical `Person` + `AboutPage` schema.

## Appendix B — Monthly SEO audit checklist

- [ ] New reviews indexed in Search Console?
- [ ] Any 404s or soft-404s?
- [ ] Core Web Vitals all green on mobile?
- [ ] Schema errors in Rich Results Test?
- [ ] AI-search audit run? (see §9)
- [ ] `dateModified` updated on any re-verified review?
- [ ] Internal links: every new review linked from at least one pillar and one sibling?
- [ ] Backlinks: any new ones worth a thank-you email to the author?
