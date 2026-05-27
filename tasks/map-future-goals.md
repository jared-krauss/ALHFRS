
## News Tab — Wayback Machine URLs

For each article in `data/news/gmail-research-threads.json`, add a `url_wayback` field where possible.

Wayback Machine URL format:
```
https://web.archive.org/web/*/ORIGINAL_URL
```

Or for a specific snapshot (auto-redirect to nearest):
```
https://web.archive.org/web/ORIGINAL_URL
```

**Goal:** In the news panel (`#news-panel` in `map-embed.html`), show a "📦 Archive" link alongside the canonical URL for articles at risk of link rot.

**Implementation:**
1. For each article in the JSON, check Wayback Machine availability API:
   `https://archive.org/wayback/available?url=URL`
2. If `closest.available == true`, store the snapshot URL as `url_wayback`
3. In `renderNewsCard()` in map-embed.html, add: if `url_wayback` exists, render a small secondary link after the article title

This can be done as a one-time enrichment script (`scripts/enrich-news-wayback.py`) that patches the JSON in place.
