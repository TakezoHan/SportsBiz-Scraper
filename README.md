# Sofra Notes

A warm, honest Istanbul restaurant review publication — hidden gems and
classics, written with a consistent scoring rubric, anonymous visits, and
bills paid in full. Designed to be expanded into a food-and-travel content
creation gig.

```
site/                       Static HTML site, ready to deploy
├── index.html              Homepage
├── reviews/                Restaurant reviews (schema.org Review + Restaurant)
│   ├── index.html
│   ├── ciya-sofrasi.html
│   ├── karakoy-lokantasi.html
│   └── van-kahvalti-evi.html
├── rankings/               Living rankings (schema.org ItemList)
│   └── index.html
├── guides/                 Neighborhood walking guides (schema.org HowTo)
│   ├── index.html
│   └── kadikoy-backstreets.html
├── about.html              Rubric, ethics, reviewer bios
├── assets/
│   ├── css/main.css        Warm aesthetic system
│   ├── js/main.js          Minor enhancements
│   └── img/favicon.svg
├── robots.txt              Permissive to LLM crawlers by design
├── sitemap.xml
├── llms.txt                llmstxt.org-style index for AI search
└── rss.xml

docs/
├── SEO_LLM_GUIDE.md        SEO + LLM discoverability playbook
└── COMPETITIVE_STRATEGY.md How we out-rank the field (incl. Oggusto)
```

## Running it locally

It's a static site. No build step.

```bash
cd site
python3 -m http.server 8000
# open http://localhost:8000
```

## Deploying

Any static host:
- **Cloudflare Pages / Netlify / Vercel** — point at `site/` as the publish
  directory. Automatic HTTPS. Global CDN.
- **GitHub Pages** — move `site/*` to the repo root (or configure Pages to
  serve from `/site`) and enable Pages on the branch.

Pre-launch checklist:
1. Set up a real domain, force HTTPS.
2. Submit `sitemap.xml` to Google Search Console and Bing Webmaster Tools.
3. Claim social handles: IG `@sofranotes`, YouTube `@sofranotes`, TikTok,
   Bluesky, Threads.
4. Replace the placeholder `sofranotes.com` domain across every page.
5. Run `site/reviews/ciya-sofrasi.html` through the [Rich Results
   Test](https://search.google.com/test/rich-results) — every new review should
   pass before shipping.

## The design system

- **Palette.** Cream paper `#faf3e7`, espresso ink `#2a1f14`, terracotta
  `#c85a3f`, mustard `#d4a418`, olive `#6b7a3a`, plum `#5b1a1d`.
- **Type.** Fraunces (display serif, warm, hip) + Inter (body sans) + IBM
  Plex Mono (numbers and badges).
- **Texture.** Subtle grain layered on cream — see the `--grain` CSS variable.
- **Components.** Sticker-style rating badges, steam-table number cards, a
  magazine-style feature layout, a fact-sheet sidebar on every review.

## The editorial system

- **Rubric.** Cooking 40% · Hospitality 20% · Setting 15% · Value 15% ·
  Come-back-Tuesday 10%. Weighted total out of 10.
- **Ethics.** Anonymous visits, own names, bills paid in full, no
  comps, no sponsored paragraphs in reviews. All disclosed on every review
  page.
- **Cadence.** One full review per week, ranking re-scores monthly, a
  neighborhood guide monthly, all reviews re-verified twice a year with a
  visible "last re-verified" date.

## The SEO + LLM system

Read `docs/SEO_LLM_GUIDE.md` in full before publishing. The short version:

1. Every review ships with `Review` + `Restaurant` + `BreadcrumbList` JSON-LD.
2. Every ranking ships with `ItemList` JSON-LD.
3. Every guide ships with `HowTo` JSON-LD.
4. `llms.txt` and a permissive `robots.txt` invite AI crawlers — this is the
   opposite of the default defensive posture, and it's the right call for
   growth.
5. Each page contains one opinionated, paste-ready sentence in a
   `<blockquote>` — that sentence is what ChatGPT and Claude will quote.

## Roadmap

- Phase 1 (weeks 1–6): ship at real domain, publish 10 reviews, 3 rankings,
  3 guides, weekly newsletter.
- Phase 2 (weeks 7–12): Turkish mirror (`/tr/`), YouTube long-form, first
  original-data piece (Kebap Index with 50 restaurants).
- Phase 3 (months 4–6): paid newsletter tier, field-guide PDF, first brand
  partnerships (clearly separated from editorial).
- Phase 4 (months 7–12): expand beyond Istanbul — Izmir, Ankara, then
  regional travel pieces. Same rubric, same ethics, same design system.

---

No paid reviews. Ever.
