# LLM Research Queue — gmail-research-threads.json

Tasks for local LLM dispatch. Each task specifies what to find, how to verify it, and exactly what field to update.

---

## TASK-001 — Resolve news-015 canonical URL

**Status:** OPEN  
**File to update:** `data/news/gmail-research-threads.json`  
**Record:** `news-015`  
**Field to update:** `url_canonical` (currently `null`)

### What to find

A Guardian letters page published around **17 June 2025**. The email subject line captured was:

> "Letters: The rapid expansion of biometric surveillance raises serious concerns about accuracy and ethics, but oversight is patchy and voluntary"

The original share URL (`https://share.google/`) is truncated — no redirect code was preserved, so it cannot be followed.

### How to search

1. Try fetching Guardian letters pages from that date range. Typical URL patterns:
   - `https://www.theguardian.com/technology/2025/jun/17/letters-...`
   - `https://www.theguardian.com/uk-news/2025/jun/17/letters-...`
   - `https://www.theguardian.com/science/2025/jun/17/letters-...`
2. Search: `site:theguardian.com letters "biometric surveillance" "patchy" 2025`
3. Search: `theguardian.com "letters" "facial recognition" "oversight is patchy" June 2025`

### Verification criteria — confirm ALL before writing

- [ ] URL domain is `www.theguardian.com`
- [ ] Page is a **letters section** (not a news article or opinion piece by a named author)
- [ ] Published between **10 June and 24 June 2025**
- [ ] Content references **biometric surveillance** or **facial recognition** expansion
- [ ] Content references oversight being **"patchy"** or **"voluntary"** — these are the distinctive phrases from the subject line

### What to write

Once confirmed, set `url_canonical` in `data/news/gmail-research-threads.json` at record `news-015`:

```json
"url_canonical": "<canonical URL here>"
```

Do not change any other fields in that record.
